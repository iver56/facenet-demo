from flask import Flask
from flask import jsonify


app = Flask(__name__, static_folder='')


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route("/classify/", methods=['POST'])
def classify():
    return jsonify({
        'predictions': []
    })


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        debug=False
    )
