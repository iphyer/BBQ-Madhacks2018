#from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import numpy as np
# from skimage import io
from util import checker, plotHelper
import uuid
from PIL import Image
import ast

app = Flask(__name__)
#bootstrap = Bootstrap(app)

UPLOAD_FOLDER = './static/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS_IMG = set(['png', 'jpg', 'jpeg', 'gif'])
ALLOWED_EXTENSIONS_TEXT = set(['csv', 'txt'])

def allowed_file(filename, mode):
    if mode == 'img':
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_IMG
    elif mode == 'text':
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_TEXT

@app.route('/')
def index():
    return render_template('indexTest.html')

@app.route('/zoomin')
def zoomin():
    # type = request.args.get('type', default='', type=str)
    # x1 = request.args.get('x1', default=0.0, type=float)
    # y1 = request.args.get('y1', default=0.0, type=float)
    # x2 = request.args.get('x2', default=0.0, type=float)
    # y2 = request.args.get('y2', default=0.0, type=float)
    info = request.args.get('info', default="", type=str)
    scale = request.args.get('scale', default=0.0, type=float)
    path = request.args.get('path', default="", type=str)
    info_list = ast.literal_eval(info)

    # print(x1)
    # print(x2)
    # print(y1)
    # print(y2)

    print("AAAAAAAAAAAAAAAAAA")
    cropName = plotHelper.cropImg(info_list, path)
    wholeName = plotHelper.wholeImg(info_list, path)
    post = {
        'info_list' : info_list,
        'path' : path,
        'scale' : scale,
        'crop' : cropName,
        'whole' : wholeName
    }


    print(path)
    return render_template('zoomin.html', posts = [post])

@app.route('/zoominCLS')
def zoominCLS():
    # type = request.args.get('type', default='', type=str)
    # x1 = request.args.get('x1', default=0.0, type=float)
    # y1 = request.args.get('y1', default=0.0, type=float)
    # x2 = request.args.get('x2', default=0.0, type=float)
    # y2 = request.args.get('y2', default=0.0, type=float)
    predinfo = request.args.get('predinfo', default="", type=str)
    predline = request.args.get('predline', default="", type=int)
    gtinfo = request.args.get('gtinfo', default="", type=str)
    gtline = request.args.get('gtline', default="", type=int)
    scale = request.args.get('scale', default=0.0, type=float)
    path = request.args.get('path', default="", type=str)
    #print("CCC")
    #print(predinfo)
    #print(gtinfo)
    predinfo_list = ast.literal_eval(predinfo)
    gtinfo_list = ast.literal_eval(gtinfo)
    #print("BBBBBBB")
    #print(info_list)
    #print(scale)
    #print(path)

    # print(x1)
    # print(x2)
    # print(y1)
    # print(y2)

    print("AAAAAAAAAAAAAAAAAA")
    predcropName = plotHelper.cropImgCLS(predinfo_list,predline,"pred", path)
    gtcropName = plotHelper.cropImgCLS(gtinfo_list,gtline,"gt" ,path)
    wholeName = plotHelper.wholeImgCLS(gtinfo_list,predinfo_list, path)
    post = {
        'predinfo_list' : predinfo_list,
        'gtinfo_list': gtinfo_list,
        'predline': predline,
        'gtline': gtline,
        'path' : path,
        'scale' : scale,
        'cropPred' : predcropName,
        'cropGt': gtcropName,
        'whole' : wholeName
    }
    print(path)
    return render_template('zoominCLS.html', posts = [post])

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist("file")
        if len(files) != 3:
            return 'Missing Input File!'
        dirpath = app.config['UPLOAD_FOLDER'] + str(uuid.uuid1()) + "/"
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        # files[0].save(os.path.join(dirpath, "image." + files[0].filename.rsplit('.', 1)[1]))
        # files[1].save(os.path.join(dirpath, "gt." + files[1].filename.rsplit('.', 1)[1]))
        # files[2].save(os.path.join(dirpath, "pred." + files[2].filename.rsplit('.', 1)[1]))
        files[0].save(os.path.join(dirpath, "image"))
        files[1].save(os.path.join(dirpath, "gt"))
        files[2].save(os.path.join(dirpath, "pred"))
        posts = processing(files, dirpath)
        return render_template('imagemap.html', posts = [posts])


def processing(files, dirPath):
    # img = io.imread(os.path.join(dirPath, "image"))
    predArr = np.loadtxt(os.path.join(dirPath, "pred"), delimiter=',')
    gtArr = np.loadtxt(os.path.join(dirPath, "gt"), delimiter=',')
    bbox_label_names = ('111', 'dot', '100')
    correct, cls_error, loc_error, confMatrix, gtNumDefects, cls_error_list, loc_error_list = checker.evaluate_twoBBox_by_iou_kinds(gtArr, predArr, bbox_label_names, threshold_IoU=0.5)


    # print(correct)
    # print(loc_error)
    # print(cls_error)
    # print(confMatrix)
    # # print(area_loc_error_list)
    # print(gtNumDefects)
    #
    precision = 1.0 * correct / (loc_error + cls_error + correct)
    recall = 1.0 * correct / (np.sum(gtNumDefects))
    F1 = 2.0 * recall * precision / (recall + precision)

    plotHelper.plotloc(loc_error_list, dirPath)
    plotHelper.plotcls(cls_error_list, dirPath)

    imin = Image.open(os.path.join(dirPath, "image"))
    imout_loc = Image.open(os.path.join(dirPath, "loc.png"))
    imout_cls = Image.open(os.path.join(dirPath, "cls.png"))
    w1, h1 = imin.size
    w2_loc, h2_loc = imout_loc.size
    w2_cls, h2_cls = imout_cls.size
    scale_loc = 1.0 * w2_loc / w1
    scale_cls = 1.0 * w2_cls / w1
    print(len(cls_error_list))
    post = {
        'p' : float("{0:.2f}".format(precision)),
        'r' : float("{0:.2f}".format(recall)),
        'f1' : float("{0:.2f}".format(F1)),
        'loc_error' : loc_error_list,
        'cls_error' : cls_error_list,
        'path' : dirPath,
        'scaleLOC' : scale_loc,
        'scaleCLS' : scale_cls
    }



    # print("============ Performance ==============")
    # print("P : %f" % precision)
    # print("R : %f" % recall)
    # print("F1 : %f" % F1)
    # print("============ Performance ==============")
    #
    # print(cls_error_list)
    # print(loc_error_list)

    return post

if __name__ == '__main__':
    app.run(debug=True)