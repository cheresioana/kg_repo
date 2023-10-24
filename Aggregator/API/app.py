import os
import sys

from flask import Flask, jsonify, request
import json
from flask_cors import CORS
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from knowledge_extraction.EntityExtractor import EntityExtractor

app = Flask(__name__)
extractor = EntityExtractor()
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


@app.route('/keywords', methods=['POST'])
def get_keywords():
    data = request.get_json()
    print(data)
    print(data['statement'])
    entities = extractor.extract_entities(data['statement'])
    print(entities)
    return jsonify(entities)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006)
