import os

from flask import Flask, request, send_file
from flask import jsonify

from predict import Classifier
from settings import VGGFACE2_TRAIN_PATH

app = Flask(__name__, static_folder='web_app')
classifier = Classifier()


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route("/classify/", methods=['POST'])
def classify():
    base64_png = request.json.get('base64_png', None)
    if base64_png is None:
        raise Exception('Invalid base64')
    predictions = classifier.predict(base64_png)
    return jsonify({
        'predictions': predictions
    })


@app.route('/celebrities/<path:path>')
def static_celebrities_proxy(path):
    return send_file(os.path.join(VGGFACE2_TRAIN_PATH, path))


@app.route('/<path:path>')
def static_proxy(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(path)


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        debug=False  # Tensorflow may throw a tantrum if debug=True, due to multiple threads then
    )
