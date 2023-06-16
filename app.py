from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return jsonify({'name': 'Alice'})
