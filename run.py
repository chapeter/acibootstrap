from flask import Flask, redirect
import subprocess

app = Flask(__name__)


@app.route("/run", methods=['GET'])
def run():
    subprocess.call("./acibootstrap.sh")
    return redirect("http://0.0.0.0:5001", code=302)

@app.route("/tests")
def tests():
    subprocess.call("./acibootstrap-tests.sh")
    return redirect("http://0.0.0.0:5001", code=302)

@app.route("/")
def main():
    #    <a href="http://0.0.0.0:5001/tests">Run tests.yaml</a>
    return '''
    <!doctype html>
    <title>ACI BOOTSTRAP</title>
    <button onclick="window.location.href='/run'">Run</button>
    '''


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
