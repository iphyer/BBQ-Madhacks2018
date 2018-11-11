from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import numpy as np

app = Flask(__name__)
bootstrap = Bootstrap(app)

UPLOAD_FOLDER = './uploads/'
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
    return render_template('home.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist("file")
        files[0].save(os.path.join(app.config['UPLOAD_FOLDER'], "image." + files[0].filename.rsplit('.', 1)[1]))
        files[1].save(os.path.join(app.config['UPLOAD_FOLDER'], "gt." + files[1].filename.rsplit('.', 1)[1]))
        files[2].save(os.path.join(app.config['UPLOAD_FOLDER'], "pred." + files[2].filename.rsplit('.', 1)[1]))

        return 'file uploaded successfully'

def processing(files):

    image = files[0]
    gt = files[1]
    pred = files[2]
    predArr = np.loadtxt(gt, delimiter=',')
    gtArr = np.loadtxt(pred, delimiter=',')


if __name__ == '__main__':
    app.run(debug=True)