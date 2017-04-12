import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
import subprocess

UPLOAD_FOLDER = 'acibootstrap/files/vars/'
ALLOWED_EXTENSIONS = set(['xlsx'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#@app.route("/run", methods=['GET'])
#def run():
#    subprocess.call("./acibootstrap.sh")
#    return redirect("http://0.0.0.0:5000", code=302)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))
    return """
    <!doctype html>
    <title>ACI BOOTSTRAP</title>
    <h1>ACI BOOTSTRAP</h1>
    <h2>Upload Config File</h2>
    <p>Upload acibootstrap.xlsx here</p>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    <p>%s</p>
    <iframe src="http://0.0.0.0:5001" width="300" height="25"></iframe>
    <iframe src="http://0.0.0.0:8001" width="1200" height="650"></iframe>
    """ % "<br>".join(os.listdir(app.config['UPLOAD_FOLDER'],))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)