'''
python flask part 
1. Flask is the flask micorframework's core package for python web program
2. render_template provides functionality to render HTML templates and process dynamic data
3. session package provides a mechanism to store data between user requests
4. request allows us to retrieve data from the HTTP requests sent by the client
5. send_from_directory can be used to send files from a specified directory as a response
'''
from flask import Flask
from flask import render_template
from flask import session
from flask import request 
from flask import send_from_directory

'''
python basic part
1. os provides functionality for interacting with the operating system
2. hashlib contains implementations of various hash algorithms,we use the sha-1 part
3. uuid allows us to generate universally unique identifiers,we use it for unique folder name
4. secrets provides functionality for generating cryptographically secure random numbers
   we set unique key for flask and enable session
'''
import os
import hashlib
import uuid
import secrets 
import threading

from utils.infer_image_module import infer_image_backend

# Constant
app = Flask(__name__,static_folder='static')

basedir = os.path.abspath(os.path.dirname(__file__))

# Global Variables
uid = '' # indicate user id
fid = '' # indicate file id
fName = '' # indicate file name
suid = ''
bboxes = ''
frame = ''


# Set a unique key for flask program 
# app.secret_key='abcd'
app.secret_key = secrets.token_hex(16)

# index page for flask program
@app.route('/')
def index():
    session['user'] = 'LeeSin'
    return render_template("index.html")

'''
The following part is responsible for send files from specified folders to the client
Warning: Do not store any user-uploaded content or system calculation results in the static folder!
'''
UPLOAD_IMAGE_FOLDER = './sources/x_image/'
INFER_IMAGE_FOLDER = './sources/y_image/'
app.config['UPLOAD_IMAGE_FOLDER'] = UPLOAD_IMAGE_FOLDER
app.config['INFER_IMAGE_FOLDER'] = INFER_IMAGE_FOLDER

@app.route('/request_upload_image/<filename>')
def display_upload_image(filename):
    return send_from_directory(app.config['UPLOAD_IMAGE_FOLDER'],filename)

@app.route('/request_infer_image/<filename>')
def display_infer_image(filename):
    return send_from_directory(app.config['INFER_IMAGE_FOLDER'],filename)

'''
The following part is responsible for user login
'''
@app.route('/login')
def login():
    return render_template("login.html")

'''
The following part is responsible for uploading files,mainly user images.
'''
@app.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'GET':
        # browse image's default method is get,so we will render its page 
        return render_template('upload_image.html')

    # Following is the POST part
    # when user click submit button,the following codes will handle request
    global fid
    global fName
    # uid = str(uuid.uuid1())

    # planning to generate uuid by hash the file
    # uuid5 will generate sha-1 hash by specified namespace and file content
    f = request.files['file']
    print(request.files)
    # note that stream must be decoded to string
    file_content = f.stream.read()
    file_hash = hashlib.sha1(file_content).hexdigest()
    fid = str(uuid.uuid5(uuid.NAMESPACE_DNS,file_hash))
    print(fid)

    fName = fid +'.jpg'
    file_path = os.path.join(r'./sources/x_image', fName)

    # make sure the directory exist
    os.makedirs(os.path.dirname(file_path),exist_ok=True)
    print(file_path)

    # try move the pointer to the beginning of the file
    f.stream.seek(0)

    f.save(file_path)
    # fName = f.filename

    upload_image_url = '/request_upload_image/' + fName
    return render_template('display_upload_image.html',url = upload_image_url)

'''
The following part is responsible for infering image files.
After the user-uploaded file is stored, it will be sent to the inference module in the backend.
'''
@app.route('/infer_image', methods=['GET', 'POST'])
def infer_image():
    global fid
    global fName

    # set input and output path
    inputdir = app.config['UPLOAD_IMAGE_FOLDER'] + fName 
    outputdir = app.config['INFER_IMAGE_FOLDER'] + fName 

    # check whether file is already exists
    if not os.path.exists(outputdir):
        # Considering start a new thread to excute this function
        t = threading.Thread(target = infer_image_backend, args=(inputdir,outputdir,app))
        t.start()

    infer_image_url = '/request_infer_image/' + fName

    # clean fid and fName variables
    # the process should be delayed
    # fid = ''
    # fName = ''
    return render_template('display_predict_result.html',url=infer_image_url)

if __name__=='__main__':
    host = '127.0.0.1'
    app.run(host=host,debug=False)
