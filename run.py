from flask import Flask, redirect
import subprocess

app = Flask(__name__)


@app.route("/run", methods=['GET'])
def run():
    subprocess.call("./acibootstrap.sh")
    return redirect("http://0.0.0.0:5001", code=302)

@app.route("/tests")
def tests():
    subprocess.call("./acibootstrap-test.sh")
    return redirect("http://0.0.0.0:5001", code=302)

@app.route("/")
def main():
    #    <a href="http://0.0.0.0:5001/tests">Run tests.yaml</a>
    #    <button onclick="window.location.href='/tests'" class="btn btn-primary">Tests</button>

    return '''
    <!doctype html>
    <title>ACI BOOTSTRAP</title>
    <link rel="stylesheet" href="http://localhost:5000/static/css/bootstrap.min.css" />
    <style>
        section{
            background-color:#ddd;
        }
    </style>
    <body>
    <section>
    <button onclick="window.location.href='/run'" class="btn btn-primary">Run</button>
    </section>
    </body>
    </html>

    '''


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
