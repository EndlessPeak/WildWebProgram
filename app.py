from flask import Flask, render_template, session, request
import os
import hashlib # hash the picture and generate uid
import uuid
import secrets # set unique key for flask and enable session
from utils.infer_image_module import infer_image_backend

# Constant
app = Flask(__name__,static_folder='static')

basedir = os.path.abspath(os.path.dirname(__file__))

# Global Variables
uid = ''
fName = ''
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

# upload file for infer module
@app.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # when user click submit button,the following codes will handle request
        global uid
        # uid = str(uuid.uuid1())

        # planning to generate uuid by hash the file
        # uuid5 will generate sha-1 hash by specified namespace and file content
        f = request.files['file']
        print(request.files)
        # note that stream must be decoded to string
        file_content = f.stream.read()
        file_hash = hashlib.sha1(file_content).hexdigest()
        uid = str(uuid.uuid5(uuid.NAMESPACE_DNS,file_hash))
        print(uid)
        
        fname = uid +'.jpg'
        file_path = os.path.join(r'./static/sources/x_image', fname)

        # make sure the directory exist
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        print(file_path)

        # try move the pointer to the beginning of the file
        f.stream.seek(0)
        f.save(file_path)
        fName = f.filename
        return render_template('display_upload_image.html',url = file_path)
    else:
        # browse image's default method is get,so we will render its page 
        return render_template('upload_image.html')

@app.route('/infer_image', methods=['GET', 'POST'])
def infer_image():
    global uid

    # set input and output path
    inputdir = r'./static/sources/x_image/'+uid+'.jpg'
    outputdir = r'./static/sources/y_image/'+uid+'.jpg'
    print(inputdir)
    # print('./static/sources/x_image/'+fName)

    infer_image_backend(inputdir,outputdir)
    # clean uid and fName variables
    # the process should be delayed
    uid = ''

    return render_template('display_predict_result.html',url=outputdir)

if __name__=='__main__':
    host = '127.0.0.1'
    app.run(host=host,debug=False)
