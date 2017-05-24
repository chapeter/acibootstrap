import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug import secure_filename
import yaml
import subprocess
import sys
from acibootstrap import app
from acibootstrap.importvars import importvars, importvars_ss

UPLOAD_FOLDER = 'files/vars/'
ALLOWED_EXTENSIONS = set(['xlsx'])

#app = Flask(__name__)
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def writeHosts():
    with open("acibootstrap/files/vars/acibootstrap_vars_ss.yml", 'r') as file:
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

@app.route("/var_template")
def varTemplate():
    return render_template('ACI-Bootstrap-Tool.xlsx')



@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        sys.stderr.write("\nbegging import\n")
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join('acibootstrap/files/vars/', filename))
            #importvars()
            importvars_ss()
            sys.stderr.write("\nwriting Hosts file\n")
            writeHosts()
            sys.stderr.write("\nredirecting back to home\n")
            return redirect(url_for('index'))

    # with open("acibootstrap/files/vars/acibootstrap_vars.yml", 'r') as file:
    #     try:
    #         vars = yaml.load(file)
    #         apic_ip = vars['apic_ip']
    #         apic_user = vars['apic_user']
    #     except:
    #         apic_ip = None
    #         apic_user = None

    with open("acibootstrap/files/vars/acibootstrap_vars_ss.yml", 'r') as file:
        try:
            vars = yaml.load(file)
            apic_ip = vars['apic_ip']
            apic_user = vars['apic_user']
        except:
            apic_ip = None
            apic_user = None


    return """
    <!doctype html>
    <body>
    <link rel="stylesheet" href="static/css/bootstrap-theme.min.css" />
    <link rel="stylesheet" href="static/css/bootstrap.min.css" />
    <link rel="stylesheet" href="static/css/my.css" />
    <link rel="shortcut icon" href="static/css/favicon.ico">

    <script src="static/js/bootstrap.min.js"></script>

    <style>

    section{
        background-color:#ddd;
        padding-top: 10px;
        padding-left:50px;

    }

    header{
        text-align: center;
        background-color: grey;
        color:#fff;
        padding: 10px
    }

    </style>

    <title>ACI BOOTSTRAP</title>
    <header>
    <h1>ACI BOOTSTRAP</h1>
    </header>

    <section>
    <h2>Upload Config File</h2>
    <p>Upload acibootstrap.xlsx here</p>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file> <br>
          <p>
             APIC IP: %s <br>
             APIC User: %s <br>
             <hr>
          </p>
      <input type=submit value=Upload class="btn btn-primary"></p>
    </form>

    <iframe src="http://0.0.0.0:5001" width="300" height="34" frameBorder="0"></iframe>

    </section>

    <br><br>

    <br>
    <iframe src="http://0.0.0.0:8001" width="1200" height="650" frameBorder="0"></iframe>
    </body>
    """ % (apic_ip, apic_user)

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        sys.stderr.write("\nbegging import\n")
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join('acibootstrap/files/vars/', filename))
            #importvars()
            importvars_ss()
            sys.stderr.write("\nwriting Hosts file\n")
            writeHosts()
            sys.stderr.write("\nredirecting back to home\n")
            return redirect(url_for('index'))

    # with open("acibootstrap/files/vars/acibootstrap_vars.yml", 'r') as file:
    #     try:
    #         vars = yaml.load(file)
    #         apic_ip = vars['apic_ip']
    #         apic_user = vars['apic_user']
    #     except:
    #         apic_ip = None
    #         apic_user = None

    with open("acibootstrap/files/vars/acibootstrap_vars_ss.yml", 'r') as file:
        try:
            vars = yaml.load(file)
            apic_ip = vars['apic_ip']
            apic_user = vars['apic_user']
        except:
            apic_ip = None
            apic_user = None


    return """
    <!doctype html>
    <body>
    <link rel="stylesheet" href="static/css/bootstrap-theme.min.css" />
    <link rel="stylesheet" href="static/css/bootstrap.min.css" />
    <link rel="stylesheet" href="static/css/my.css" />
    <link rel="shortcut icon" href="static/css/favicon.ico">

    <script src="static/js/bootstrap.min.js"></script>

    <style>

    section{
        background-color:#ddd;
        padding-top: 10px;
        padding-left:50px;

    }

    header{
        text-align: center;
        background-color: grey;
        color:#fff;
        padding: 10px
    }

    </style>

    <title>ACI BOOTSTRAP</title>
    <header>
    <h1>ACI BOOTSTRAP</h1>
    </header>

    <section>
    <h2>Upload Config File</h2>
    <p>Upload acibootstrap.xlsx here</p>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file> <br>
          <p>
             APIC IP: %s <br>
             APIC User: %s <br>
             <hr>
          </p>
      <input type=submit value=Upload class="btn btn-primary"></p>
    </form>

    </body>
    """ % (apic_ip, apic_user)
