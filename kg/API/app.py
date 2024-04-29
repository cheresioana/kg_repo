import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from  logs import logger
from tests.populate_db import populate
from constanst import AGGREGATOR_URL

from DataObject.SubGraphResult import ComplexEncoder, ResultItem, Node, Link


from SearchEngine import SearchEngine

import random
from collections import Counter
from flask import Flask, jsonify, request
import json
from flask_cors import CORS, cross_origin
import requests
from Neo4JConnector.NeoConnector import (NeoConnector)
from ChatGPT.ChatGPTWrapper import ChatGPTWrapper
from Neo4JConnector.NeoAlgorithms import (NeoAlgorithms)
import pandas as pd
import time

app = Flask(__name__)

neo_aglo = NeoAlgorithms()
connector = NeoConnector()
chat = ChatGPTWrapper()
search_engine = SearchEngine()

CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'

#df = pd.read_csv('data/data2.csv')

@app.before_request
def before_request():
    headers = {'Access-Control-Allow-Origin': '*',
               'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
               'Access-Control-Allow-Headers': 'Content-Type'}
    if request.method.lower() == 'options':
        return jsonify(headers), 200

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
    logger.info("Get /get_kg")
    print("get kg")
    kg = connector.get_kg()
    with open("sample.json", "w") as outfile:
        json.dump(kg, outfile)
    return jsonify(kg)


@app.route('/get_similar/<id>', methods=['GET'])
def get_similar_kg(id):
    similar_list = connector.get_similar(id)
    return jsonify(similar_list)


@app.route('/analyze2', methods=['POST'])
def analyze2():
    data = request.get_json()
    logger.info(f"analyze2 {data}")

    start_time = time.time()
    keywords, show_links, show_nodes, path_result, origin_node = search_engine.find_results(data['statement'])
    duration = time.time() - start_time
    logger.info(f"The search took {duration} seconds to run.")
    print(f"The search took {duration} seconds to run.")
    json_response = {
        'origin': [origin_node],
        'keywords': keywords,
        'all_results': path_result
    }
    json_str = json.dumps(json_response, cls=ComplexEncoder, indent=4)
    return json_str


@app.route('/load_more', methods=['POST'])
def load_more():
    data = request.get_json()
    logger.info(f"analyze2 {data}")
    start_time = time.time()
    keywords, show_links, show_nodes, path_result, origin_node = search_engine.find_results(data['statement'], data['skip'])
    duration = time.time() - start_time
    logger.info(f"The search took {duration} seconds to run.")
    print(f"The search took {duration} seconds to run.")
    json_response = {
        'origin': [origin_node],
        'keywords': keywords,
        'all_results': path_result
    }
    json_str = json.dumps(json_response, cls=ComplexEncoder, indent=4)
    return json_str


# @app.route('/node_info/<id>', methods=['GET'])
# def get_node_info(id):
#     res = df[df['id'] == int(id)]
#     if len(res) == 0:
#         return jsonify([])
#     res.fillna(0, inplace=True)
#     result = res.iloc[0]
#
#     return jsonify(result.to_dict())


@app.route('/addStatement', methods=['POST'])
def addStatement():
    logger.info("ADD STATEMENT")
    data = request.get_json()
    print(data)
    intra_id = data['intra_id']
    query_node = Node(data['origin']['intra_id'], data['origin']['statement'], data['origin']['id'])
    # parsed_data = json.loads(data["all_results"])
    result_items = [
        ResultItem(
            item_data['weight'],
            item_data['intra_id'],
            item_data['query_id'],
            item_data['statement'],
            [Node(**node) for node in item_data['nodes']],  # Convert each dict to a Node instance
            [Link(**link) for link in item_data['links']],  # Convert each dict to a Link instance
            selected=item_data.get('selected', 0),# using .get() in case 'selected' is not present
            date=item_data.get('date', ""),
            channel=item_data.get('channel', ""),
            location=item_data.get('location', ""),
            url=item_data.get('url', "")
        )
        for item_data in data["all_results"]
    ]
    show_nodes = []
    show_links = []
    for result_item in result_items:
        if result_item.selected == 1:
            show_nodes.extend(result_item.nodes)
            show_links.extend(result_item.links)
        elif result_item.intra_id == intra_id:
            show_nodes.extend(result_item.nodes)
            show_links.extend(result_item.links)
            result_item.selected = 1
    show_links = list(set(show_links))
    show_nodes = (list(set(show_nodes)))
    show_nodes.append(query_node)
    json_response = {
        'origin': [query_node],
        'keywords': data['keywords'],
        'links': show_links,
        'nodes': show_nodes,
        'all_results': result_items
    }

    print(result_items[0].weight)
    print(result_items[0].statement)

    json_str = json.dumps(json_response, cls=ComplexEncoder, indent=4)
    return json_str


@app.route('/removeStatement', methods=['POST'])
def removeStatement():
    print("REMOVE")
    data = request.get_json()
    print(data)
    intra_id = data['intra_id']
    query_node = Node(data['origin']['intra_id'], data['origin']['statement'], data['origin']['id'])
    # parsed_data = json.loads(data["all_results"])
    result_items = [
        ResultItem(
            item_data['weight'],
            item_data['intra_id'],
            item_data['query_id'],
            item_data['statement'],
            [Node(**node) for node in item_data['nodes']],  # Convert each dict to a Node instance
            [Link(**link) for link in item_data['links']],  # Convert each dict to a Link instance
            selected=item_data.get('selected', 0),  # using .get() in case 'selected' is not present
            date=item_data.get('date', ""),
            channel=item_data.get('channel', ""),
            location=item_data.get('location', ""),
            url=item_data.get('url', "")
        )
        for item_data in data["all_results"]
    ]
    show_nodes = []
    show_links = []
    for result_item in result_items:
        if result_item.intra_id == intra_id:
            result_item.selected = 0
        elif result_item.selected == 1:
            show_nodes.extend(result_item.nodes)
            show_links.extend(result_item.links)

    show_links = list(set(show_links))
    show_nodes = (list(set(show_nodes)))
    show_nodes.append(query_node)
    json_response = {
        'origin': [query_node],
        'keywords': data['keywords'],
        'links': show_links,
        'nodes': show_nodes,
        'all_results': result_items
    }

    print(result_items[0].weight)
    print(result_items[0].statement)

    json_str = json.dumps(json_response, cls=ComplexEncoder, indent=4)
    return json_str

@app.route('/init_db', methods=['GET'])
def init_db():
    populate()
    return jsonify([])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
