import sys
import os
import threading
import traceback
import time
import queue

from DataObject.SubGraphResult import ComplexEncoder, ResultItem, Node, Link

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from SearchEngine import SearchEngine

try:
    from _queue import SimpleQueue
except ImportError:
    SimpleQueue = None
import grpc
from concurrent import futures
import data_formats_pb2 as pb
import data_formats_pb2_grpc as grcp_pb
import random
from collections import Counter
from flask import Flask, jsonify, request
import json
from flask_cors import CORS
import requests
from Neo4JConnector.NeoConnector import (NeoConnector)
from ChatGPT.ChatGPTWrapper import ChatGPTWrapper
from Neo4JConnector.NeoAlgorithms import (NeoAlgorithms)
import pandas as pd
import logging

app = Flask(__name__)

neo_aglo = NeoAlgorithms()
connector = NeoConnector()
chat = ChatGPTWrapper()
CORS(app)

df = pd.read_csv('../data/data2.csv')


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
    return jsonify(kg)


@app.route('/get_similar/<id>', methods=['GET'])
def get_similar_kg(id):
    similar_list = connector.get_similar(id)
    return jsonify(similar_list)


@app.route('/analyze/<statement>', methods=['GET'])
def analyze(statement):
    data = {"statement": statement}
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
        # debunk = chat.create_debunk(data['statement'])
        dic = {
            'keywords': merged_list,
            'subgraf': subgraf,
            'debunk': debunk
        }
        return jsonify(dic)
    else:
        print("Failed to send data")
    return jsonify([])


@app.route('/analyze2/<statement>', methods=['GET'])
def analyze2(statement):
    print("Statement received")
    print(statement)
    search_engine = SearchEngine()
    my_statement = pb.Statement()
    my_statement.type = statement
    js_to_protobuf_queue.put(my_statement)
    print("... sent")

    '''keywords, show_links, show_nodes, path_result, origin_node = search_engine.find_results(statement)
    json_response = {
        'origin': [origin_node],
        'keywords': keywords,
        'links': show_links,
        'nodes': show_nodes,
        'all_results': path_result
    }
    json_str = json.dumps(json_response, cls=ComplexEncoder, indent=4)
    with open("mihai.json", "w") as json_file:
        json.dump(json_response, json_file, cls=ComplexEncoder, indent=2)
    return json_str'''
    return None


@app.route('/node_info/<id>', methods=['GET'])
def get_node_info(id):
    res = df[df['id'] == int(id)]
    if len(res) == 0:
        return jsonify([])
    res.fillna(0, inplace=True)
    result = res.iloc[0]

    return jsonify(result.to_dict())


@app.route('/addStatement', methods=['POST'])
def addStatement():
    print("ADD STATEMENT")
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
            location=item_data.get('location', "")
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
            location=item_data.get('location', "")
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


class MainKGImp(grcp_pb.MainKG):
    def __init__(self, to_protobuf_queue, to_js_queue):
        self.to_protobuf_queue = to_protobuf_queue
        self.to_js_queue = to_js_queue

    def RequestKeywords(self, request, context):
        print("Enters request keywords")
        try:
            while True:
                try:

                    # make sure we notice that the connection is gone if the orchestrator dies
                    ret = self.to_protobuf_queue.get(block=True, timeout=1.0)
                    print("received ret")
                    print(ret)
                    return ret
                except queue.Empty:
                    if not context.is_active():
                        raise RuntimeError("RPC interrupted - leaving requestSudokuEvaluation")
                    # otherwise continue
        except Exception:
            print("got exception %s", traceback.format_exc())
            time.sleep(1)
            pass


protobuf_to_js_queue = queue.Queue()
js_to_protobuf_queue = queue.Queue()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    grcp_pb.add_MainKGServicer_to_server(MainKGImp(js_to_protobuf_queue, protobuf_to_js_queue), server)
    server.add_insecure_port('[::]:8061')  # Change the port if needed
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    grpc_thread = threading.Thread(target=serve)
    print("Started server")
    grpc_thread.start()

    app.run(port=8062, use_reloader=False)
    grpc_thread.join()
