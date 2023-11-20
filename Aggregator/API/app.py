import os
import sys

from flask import Flask, jsonify, request
import json
from flask_cors import CORS
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from knowledge_extraction.EntityExtractor import EntityExtractor
from  logs import logger

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
    logger.info(f"Called get keywords from aggregator {data}")
    entities = extractor.extract_entities(data['statement'])
    keyword = extractor.get_keywords_from_text(data['statement'], entities)

    if keyword.get('simple_keyword') is not None:
        entities['simple_keyword'] = keyword['simple_keyword']
    logger.info(f"Response aggregator {entities}")
    return jsonify(entities)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006)
