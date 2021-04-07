# Authors: CS For Insight (Summer19 - JG)

try:
    from flask import render_template, redirect, url_for, request, send_from_directory, flash
except:
    print("Not able to import all of the calls needed from the Flask library.")

from app import app
import os

from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

try:
    from PIL import Image
    import PIL.ImageOps
except:
    print("Make sure to pip install Pillow")

from app import pythonfunctions  # our Python functions are in pythonfunctions.py


# Home page, renders the index.html template
@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html', title='Home')

# Pig latin page, when we click translate, moves to text result page
@app.route('/text',methods=['GET','POST'])
def text():
    if request.method == 'POST':
        old_text = request.form['text']
        new_text = pythonfunctions.pig_translate(old_text)
        return render_template('textResults.html', old_text=old_text, new_text=new_text)
    return render_template('text.html', title='Home')

# Substitutions page, when we click submit, it substitutes!
@app.route('/subs',methods=['GET','POST'])
def subs():
    if request.method == 'POST':
        # larger textarea
        old_textarea = request.form['textarea_input']
        # old words and new words (their replacements)
        old_word1 = request.form['original_text1']
        old_word2 = request.form['original_text2']
        old_word3 = request.form['original_text3']
        new_word1 = request.form['replacement_text1']
        new_word2 = request.form['replacement_text2']
        new_word3 = request.form['replacement_text3']
        # create a dictionary of substitutions
        substitutions = {}
        substitutions[old_word1] = new_word1
        substitutions[old_word2] = new_word2
        substitutions[old_word3] = new_word3
        # do the transformation in Python
        new_text = pythonfunctions.substitute(old_textarea, substitutions)
        return render_template('subsResults.html', 
                                old_text=old_textarea, 
                                new_text=new_text)
    else:
        return render_template('subs.html', title='Home')

# Used for uploading pictures
@app.route('/<filename>')
def get_file(filename):
    return send_from_directory('static',filename)

# Image uploading page, 
@app.route('/image', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        # if the image is valid, do the following
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Create a path to the image in the upload folder, save the upload
            # file to this path
            save_old=(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(save_old)
            # Take the image, make a new one that is inverted
            img = Image.open(save_old)
            rbg_img = img.convert('RGB')
            inverted_image = PIL.ImageOps.invert(rbg_img)
            save_new=(os.path.join(app.config['UPLOAD_FOLDER'], 'new_'+filename))
            inverted_image.save(save_new)
            # Render template with inverted picture
            rt = render_template('imageResults.html', filename='new_'+filename)
            return rt
    return render_template('image.html')

# allowed image types 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app.config['ALLOWED_EXTENSIONS']=ALLOWED_EXTENSIONS

# is file allowed to be uploaded?
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']