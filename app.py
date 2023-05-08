import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image, ImageDraw, ImageFont

UPLOAD_FOLDER = 'uploads/'
RESULTS_FOLDER = 'static/results/'
DOWNLOADS_FOLDER = 'static/downloads/'

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER
app.config['DOWNLOADS_FOLDER'] = DOWNLOADS_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def add_logo(image_path, logo_path):
    im = Image.open(image_path)
    logo = Image.open(logo_path)
    logo_size = min(im.size) // 4
    logo.thumbnail((logo_size, logo_size))
    im.paste(logo, (im.size[0]-logo.size[0], im.size[1]-logo.size[1]), logo)
    result_path = os.path.join(app.config['RESULTS_FOLDER'], 'result.jpg')
    im.save(result_path)
    return result_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_image', methods=['POST'])
def upload_image():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return redirect(url_for('results', filename=filename))
    else:
        return redirect(url_for('index'))

@app.route('/results/<filename>')
def results(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    logo_path = os.path.join(app.root_path, 'static', 'logo.png')
    result_path = add_logo(file_path, logo_path)
    return render_template('result.html', result_path=result_path)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/results/<filename>')
def result_file(filename):
    return send_from_directory(app.config['RESULTS_FOLDER'], filename)

# @app.route('/downloads/<filename>')
# def download_file(filename):
#     return send_from_directory(app.config['DOWNLOADS_FOLDER'], filename, as_attachment=True)
if __name__ == '__main__':
    app.run()
