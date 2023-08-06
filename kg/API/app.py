import os
import random
import sys

from flask import Flask, jsonify, request
import json
from flask_cors import CORS

sys.path.append(os.path.dirname(os.path.abspath('/home/ioana/kg_repo/kg/Neo4JConnector')))
from Neo4JConnector.NeoConnector import (NeoConnector)

app = Flask(__name__)

connector = NeoConnector()
CORS(app)


# Sample data
def load_kg():
    with open('../kg.json', 'r') as file:
        data = json.load(file)
        file.close()
    return data


@app.route('/sample_kg', methods=['GET'])
def get_sample_kg():
    N = 10  # or whatever value you want

    gData = {
        "nodes": [{"id": i} for i in range(N)],
        "links": [
            {
                "source": id,
                "target": round(random.random() * (id - 1))
            }
            for id in range(1, N)  # Python's range is [start, end) exclusive the end.
        ]
    }

    return jsonify(gData)


@app.route('/get_kg', methods=['GET'])
def get_kg():
    kg = connector.get_kg()
    print(kg)
    return jsonify(kg)

@app.route('/get_similar/<id>', methods=['GET'])
def get_similar_kg(id):
    similar_list = connector.get_similar(id)
    print(similar_list)
    return jsonify(similar_list)

if __name__ == '__main__':
    app.run(port=5005)
