from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import numpy as np
from skimage import io
from util import checker, plotHelper
import uuid


app = Flask(__name__)
bootstrap = Bootstrap(app)

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
        return "123"


def processing(files, dirPath):
    img = io.imread(os.path.join(dirPath, "image"))
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

    plotHelper.plot(loc_error_list, dirPath)

    post = {
        'p' : precision,
        'r' : recall,
        'f1' : F1,
        'loc_error' : loc_error_list,
        'path' : dirPath
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