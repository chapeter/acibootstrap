import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
import yaml
import subprocess
import sys

UPLOAD_FOLDER = 'acibootstrap/files/vars/'
ALLOWED_EXTENSIONS = set(['xlsx'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def writeHosts():
    with open("acibootstrap/files/vars/acibootstrap_vars.yml", 'r') as file:
        try:
            vars = yaml.load(file)
            apic_ip = vars['apic_ip']
            apic_user = vars['apic_user']
            apic_pass = vars['apic_pass']
        except:
            apic_ip = None
            apic_user = None
            apic_pass = None

    content = '''
    [apic]
    {0}

    [all:vars]
    user = {1}
    pass = {2}
    '''.format(apic_ip, apic_user, apic_pass)

    file = open("acibootstrap/files/vars/hosts", "w")
    file.write(content)
    file.close()

    return


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            subprocess.call("acibootstrap/importvars.py")
            writeHosts()
            return redirect(url_for('index'))

    with open("acibootstrap/files/vars/acibootstrap_vars.yml", 'r') as file:
        try:
            vars = yaml.load(file)
            apic_ip = vars['apic_ip']
            apic_user = vars['apic_user']
        except:
            apic_ip = None
            apic_user = None


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
    <p>
       APIC IP: %s <br>
       APIC User: %s <br>
    </p>
    <iframe src="http://0.0.0.0:5001" width="300" height="25"></iframe>
    <iframe src="http://0.0.0.0:8001" width="1200" height="650"></iframe>
    """ % ("<br>".join(os.listdir(app.config['UPLOAD_FOLDER'],)), apic_ip, apic_user)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
