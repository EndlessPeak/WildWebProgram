from flask import Flask, render_template, session, request
from flask import send_from_directory
import secrets
import uuid
import os

app = Flask(__name__,static_folder='static')

# Set a unique key for flask program 
# app.secret_key='abcd'
app.secret_key = secrets.token_hex(16)

# index page for flask program
@app.route('/')
def index():
    session['user'] = 'LeeSin'
    return render_template("index.html")

# upload file for infer module
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        global uid
        uid = str(uuid.uuid1())
        f = request.files['file']
        print(request.files)
        fname = uid +'.JPG'
        file_path = os.path.join(r'./static/sources/x_image', fname)
        print(file_path)
        f.save(file_path)
        fName = f.filename
        return render_template('showimg.html',url = file_path)
    else:
        return render_template('upload.html')


if __name__=='__main__':
    host = '127.0.0.1'
    app.run(host=host,debug=False)
