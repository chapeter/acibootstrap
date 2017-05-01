import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug import secure_filename
import yaml
import subprocess
import sys
from acibootstrap import app

UPLOAD_FOLDER = 'files/vars/'
ALLOWED_EXTENSIONS = set(['xlsx'])

#app = Flask(__name__)
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

@app.route("/portmap")
def portmap():
    return render_template('portmap.html')



@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join('acibootstrap/files/vars/', filename))
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

    # used to show files in dir
    # <iframe src="http://0.0.0.0:8001" width="1200" height="650"></iframe>

    return """
    <!doctype html>

    <link rel="stylesheet" href="aciboostrap/static/css/bootstrap.min.css">
    <link rel="stylesheet" href="aciboostrap/static/css/bootstrap-theme.min.css">
    <script src="/js/bootstrap.min.js"></script>

    <title>ACI BOOTSTRAP</title>
    <h1>ACI BOOTSTRAP</h1>
    <h2>Upload Config File</h2>
    <p>Upload acibootstrap.xlsx here</p>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    <p>
       APIC IP: %s <br>
       APIC User: %s <br>
    </p>
    <iframe src="http://0.0.0.0:5001" width="300" height="40" frameBorder="0"></iframe>
    <br><br>
    <iframe src="http://0.0.0.0:8001" width="1200" height="650" frameBorder="0"></iframe>
    """ % (apic_ip, apic_user)
