import os
import glob
from classify import prediction
import tensorflow as tf
import  _thread
import time
# We'll render HTML templates and access data sent by POST
# using the request object from flask. Redirect and url_for
# will be used to redirect the user once the upload is done 
# and send_from_directory will help us to send/show on the
# browser the file that the user just uploaded
from flask import Flask, render_template, request, redirect, url_for, send_from_directory,flash
from werkzeug.utils import secure_filename
# Initialize the Flask application
app = Flask(__name__, )
# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['jpg', 'jpeg'])
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cap')
def capture():
    return render_template('cap.html')


# Route that will process the file upload
@app.route('/uploads', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
   
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        filename  = str(len(os.listdir(app.config['UPLOAD_FOLDER']))+1)+'.jpg'
        # Move the file form the temporal folder to
        # the upload folder we setup
        file_name_full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_name_full_path)
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        return render_template('upload_success.html')

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/claim', methods=['POST'])
def predict():
    image_path = max(glob.glob(r'uploads\*jpg'), key=os.path.getctime)
    with tf.Graph().as_default():
        human_string, score= prediction(image_path)
    print('model one value' + str(human_string))
    print('model one value' + str(score))
    if (human_string == ' '):
        label_text = 'This is not  ' + str(score) + '%. Please upload  image'
        print(image_path)
        return render_template('front.html', text = label_text, filename= image_path)
    elif (human_string == 'adulterated bad'):
        text01 = 'เป็นข้าวสารที่มีสิ่งเจือปน คุณภาพต่ำ'
        text02 = 'ความถูกต้อง '+ str(score) + ' %'
        print(image_path)
        return render_template('front.html', text1 = text01, text2 = text02, filename= image_path)
    elif (human_string == 'adulterated good'):
        text01 = 'เป็นข้าวสารที่มีสิ่งเจือปน คุณภาพดี'
        text02 = 'ความถูกต้อง '+ str(score) + ' %'
        print(image_path)
        return render_template('front.html', text1 = text01, text2 = text02, filename= image_path)
    elif (human_string == 'adulterated medium'):
        text01 = 'เป็นข้าวสารที่มีสิ่งเจือปน คุณภาพปานกลาง'
        text02 = 'ความถูกต้อง '+ str(score) + ' %'
        return render_template('front.html', text1 = text01, text2 = text02, filename= image_path)
    elif (human_string == 'unadulterated bad'):
        text01 = 'เป็นข้าวสารที่ไม่มีสิ่งเจือปน คุณภาพต่ำ'
        text02 = 'ความถูกต้อง '+ str(score) + ' %'
        return render_template('front.html', text1 = text01, text2 = text02, filename= image_path)
    elif (human_string == 'unadulterated good'):
        text01 = 'เป็นข้าวสารที่ไม่มีสิ่งเจือปน คุณภาพดี'
        text02 = 'ความถูกต้อง '+ str(score) + ' %'
        return render_template('front.html', text1 = text01, text2 = text02, filename= image_path)
    elif (human_string == 'unadulterated medium'):
        text01 = 'เป็นข้าวสารที่ไม่มีสิ่งเจือปน คุณภาพปานกลาง'
        text02 = 'ความถูกต้อง '+ str(score) + ' %'
        return render_template('front.html', text1 = text01, text2 = text02, filename= image_path)
if __name__ == '__main__':
    app.debug = True
    app.run(host="")


