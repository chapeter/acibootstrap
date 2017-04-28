from acibootstrap import app

UPLOAD_FOLDER = 'acibootstrap/files/vars/'

app.secret_key = '1234'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.run(host='0.0.0.0', port=5000, debug=True)
