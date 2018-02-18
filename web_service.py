from flask import Flask, send_from_directory
from flask import jsonify

app = Flask(__name__, static_folder='web_app')


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route("/classify/", methods=['POST'])
def classify():
    return jsonify({
        'predictions': []
    })


@app.route('/<path:path>')
def static_proxy(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(path)


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        debug=True
    )
