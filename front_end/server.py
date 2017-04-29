import os
from flask import Flask, request, redirect, url_for, send_from_directory,flash
from werkzeug.utils import secure_filename

# Setup Flask app.
app = Flask(__name__)
UPLOAD_FOLDER = "../front_end/upload"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS= set(['txt','jpg', 'jpeg'])

app.debug = True


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Routes
@app.route('/')
def root():
  return app.send_static_file('index.html')

@app.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/', methods=[ 'GET','POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file You idiot')
            return redirect(request.url)
        if file and allowed_file(file.filename):#triggered if the allowed file is uploaded
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            with open(os.path.join(UPLOAD_FOLDER, filename), 'r') as myfile:
                data=myfile.read().replace("\n", "")

            f = open( 'input.txt', 'w' )
            f.write( data )
            f.close()

            #return redirect(url_for('uploaded_file',filename=filename))



        return app.send_static_file('index.html')





@app.route('/<path:path>')
def static_proxy(path):
  # send_static_file will guess the correct MIME type
  return app.send_static_file(path)


if __name__ == '__main__':
    app.run(host= "0.0.0.0")
