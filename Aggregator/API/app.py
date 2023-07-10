from flask import Flask, jsonify, request
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Sample data
def load_kg():
    with open('../kg.json', 'r') as file:
        data = json.load(file)
        file.close()
    return data

@app.route('/kg', methods=['GET'])
def get_kg():
    nodes = load_kg()
    return jsonify(nodes)