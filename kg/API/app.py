import os
import random
import sys
from collections import Counter

from flask import Flask, jsonify, request
import json
from flask_cors import CORS
import requests



sys.path.append(os.path.dirname(os.path.abspath('/home/ioana/kg_repo/kg/Neo4JConnector')))
from Neo4JConnector.NeoConnector import (NeoConnector)
sys.path.append(os.path.dirname(os.path.abspath('/home/ioana/kg_repo/kg/ChatGPT')))
from ChatGPT.ChatGPTWrapper import ChatGPTWrapper

app = Flask(__name__)

from Neo4JConnector.NeoAlgorithms import (NeoAlgorithms)

neo_aglo = NeoAlgorithms()
connector = NeoConnector()
chat = ChatGPTWrapper()
CORS(app)

import pandas as pd

df = pd.read_csv('data.csv')

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
    #print(kg)
    return jsonify(kg)


@app.route('/get_similar/<id>', methods=['GET'])
def get_similar_kg(id):
    similar_list = connector.get_similar(id)
    #print(similar_list)
    return jsonify(similar_list)


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    print(data)
    print(data['statement'])
    response = requests.post("http://127.0.0.1:5006/keywords", json=data)
    if response.status_code == 200:
        entities = response.json()
        statement_id = connector.insert_search_statement(data['statement'])
        print(statement_id)
        connector.insert_statement_entities(statement_id, entities)
        print(response.json())
        print(entities.values)
        merged_list = [value for sublist in entities.values() for value in sublist]
        print(merged_list)

        # connector.set_similarity()
        # connector.run_louvain_algorithm()
        connector.del_similar_rel()
        neo_aglo.knn()
        res = neo_aglo.find_similar(statement_id)
        selected_communities = [r['community'] for r in res]
        selected_communities = list(filter(lambda x: x is not None, selected_communities))
        counter = Counter(selected_communities)
        selected_community = -1
        if len(selected_communities) > 0:
            print("community detected")

            selected_community = counter.most_common(1)[0][0]
            print(selected_community)
            subgraf = connector.get_community_detected_subgraph(statement_id, selected_community)
        else:
            print("community NOT detected")
            subgraf = connector.get_community_not_detected_subgraph(statement_id)
        debunk = 'save the money'
        debunk = chat.create_debunk(data['statement'])
        dic = {
            'keywords': merged_list,
            'subgraf': subgraf,
            'debunk': debunk
        }
        return jsonify(dic)
    else:
        print("Failed to send data")
    return jsonify([])

@app.route('/node_info/<id>', methods=['GET'])
def get_node_info(id):
    print(id)

    res = df[df['id'] == int(id)]
    if len(res) == 0:
        return jsonify([])
    res.fillna(0, inplace=True)
    result = res.iloc[0]
    print(result['statement'])
    return jsonify(result.to_dict())

if __name__ == '__main__':
    app.run(port=5005)
