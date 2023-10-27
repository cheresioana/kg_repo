import sys
import os
import threading
import traceback
import time
import queue

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from DataObject.SubGraphResult import ComplexEncoder, ResultItem, Node, Link
# from tests.populate_db import populate_db
#
#
# from SearchEngine import SearchEngine
# from google.protobuf import json_format
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

# neo_aglo = NeoAlgorithms()
# connector = NeoConnector()
# chat = ChatGPTWrapper()
CORS(app)

#df = pd.read_csv('data/data2.csv')


# @app.route('/sample_kg', methods=['GET'])
# def get_sample_kg():
#     N = 10  # or whatever value you want
#
#     gData = {
#         "nodes": [{"id": i} for i in range(N)],
#         "links": [
#             {
#                 "source": id,
#                 "target": round(random.random() * (id - 1))
#             }
#             for id in range(1, N)  # Python's range is [start, end) exclusive the end.
#         ]
#     }
#
#     return jsonify(gData)
#
#
# @app.route('/get_kg', methods=['GET'])
# def get_kg():
#     kg = connector.get_kg()
#     return jsonify(kg)
#
#
# @app.route('/get_similar/<id>', methods=['GET'])
# def get_similar_kg(id):
#     similar_list = connector.get_similar(id)
#     return jsonify(similar_list)


# @app.route('/analyze/<statement>', methods=['GET'])
# def analyze(statement):
#     data = {"statement": statement}
#     my_statement = pb.Statement()
#     my_statement.type = statement
#     js_to_protobuf_queue.put(my_statement)
#     print("... sent")
#
#     ret = None
#     while True:
#         try:
#             print("wait_update")
#             ret = protobuf_to_js_queue.get(block=True, timeout=1)
#             print("GUI got update from protobuf!")
#             print(ret)
#             statement_node = connector.insert_search_statement(statement)
#             print(statement_node.intra_id)
#             connector.insert_statement_entities(statement_id, entities)
#             print(response.json())
#             print(entities.values)
#             merged_list = [value for sublist in entities.values() for value in sublist]
#             print(merged_list)
#
#             # connector.set_similarity()
#             # connector.run_louvain_algorithm()
#             connector.del_similar_rel()
#             neo_aglo.knn()
#             res = neo_aglo.find_similar(statement_id)
#             selected_communities = [r['community'] for r in res]
#             selected_communities = list(filter(lambda x: x is not None, selected_communities))
#             counter = Counter(selected_communities)
#             selected_community = -1
#             if len(selected_communities) > 0:
#                 print("community detected")
#
#                 selected_community = counter.most_common(1)[0][0]
#                 print(selected_community)
#                 subgraf = connector.get_community_detected_subgraph(statement_id, selected_community)
#             else:
#                 print("community NOT detected")
#                 subgraf = connector.get_community_not_detected_subgraph(statement_id)
#             debunk = 'save the money'
#             # debunk = chat.create_debunk(data['statement'])
#             dic = {
#                 'keywords': merged_list,
#                 'subgraf': subgraf,
#                 'debunk': debunk
#             }
#             return jsonify(dic)
#         except queue.Empty:
#             pass

    #response = requests.post("http://127.0.0.1:5006/keywords", json=data)
    # if response.status_code == 200:
    #     entities = response.json()
    #     print("received response")
    #     print(entities)
    #     statement_id = connector.insert_search_statement(data['statement'])
    #     print(statement_id)
    #     connector.insert_statement_entities(statement_id, entities)
    #     print(response.json())
    #     print(entities.values)
    #     merged_list = [value for sublist in entities.values() for value in sublist]
    #     print(merged_list)
    #
    #     # connector.set_similarity()
    #     # connector.run_louvain_algorithm()
    #     connector.del_similar_rel()
    #     neo_aglo.knn()
    #     res = neo_aglo.find_similar(statement_id)
    #     selected_communities = [r['community'] for r in res]
    #     selected_communities = list(filter(lambda x: x is not None, selected_communities))
    #     counter = Counter(selected_communities)
    #     selected_community = -1
    #     if len(selected_communities) > 0:
    #         print("community detected")
    #
    #         selected_community = counter.most_common(1)[0][0]
    #         print(selected_community)
    #         subgraf = connector.get_community_detected_subgraph(statement_id, selected_community)
    #     else:
    #         print("community NOT detected")
    #         subgraf = connector.get_community_not_detected_subgraph(statement_id)
    #     debunk = 'save the money'
    #     # debunk = chat.create_debunk(data['statement'])
    #     dic = {
    #         'keywords': merged_list,
    #         'subgraf': subgraf,
    #         'debunk': debunk
    #     }
    #     return jsonify(dic)
    # else:
    #     print("Failed to send data")
    #return jsonify([])

from google.protobuf.descriptor import FieldDescriptor
def grpc_message_to_dict(message):
    """
    Convert a gRPC message to a Python dictionary.
    """
    message_dict = {}
    for field in message.DESCRIPTOR.fields:
        field_value = getattr(message, field.name)

        # Check if the field is another message and convert it as well
        if field.type == field.TYPE_MESSAGE:
            if field.label == field.LABEL_REPEATED:
                message_dict[field.name] = [grpc_message_to_dict(f) for f in field_value]
            else:
                message_dict[field.name] = grpc_message_to_dict(field_value)
        else:
            if field.label == field.LABEL_REPEATED:
                message_dict[field.name] = list(field_value)
            else:
                message_dict[field.name] = field_value

    return message_dict

# @app.route('/analyze2/<statement>', methods=['GET'])
# def analyze2(statement):
#     print("Statement received")
#     print(statement)
#     search_engine = SearchEngine()
#     my_statement = pb.Statement()
#     my_statement.type = statement
#     js_to_protobuf_queue.put(my_statement)
#     print("... sent")
#     print("wait_update")
#     while True:
#         try:
#
#             ret = protobuf_to_js_queue.get(block=True, timeout=1)
#             print("GUI got update from protobuf!")
#             print(ret)
#             break
#         except queue.Empty:
#             pass
#
#
#     entities = grpc_message_to_dict(ret)
#     print("dict format")
#     print(entities)
#     new_dic = {}
#     for ent in entities['entities']:
#         print(ent)
#         print(ent['type'])
#         print(ent['values'])
#         new_dic[ent['type']] = ent['values']
#
#     print('converted dict')
#     print(new_dic)
#     entities = new_dic
#     query_node = connector.insert_search_statement(statement)
#     connector.insert_statement_entities(query_node.intra_id, entities)
#     print("inserted query node")
#     print("inserted entities")
#
#     keywords, show_links, show_nodes, path_result, origin_node = search_engine.find_results(statement, query_node, entities)
#     json_response = {
#         'origin': [origin_node],
#         'keywords': keywords,
#         'links': show_links,
#         'nodes': show_nodes,
#         'all_results': path_result
#     }
#     json_str = json.dumps(json_response, cls=ComplexEncoder, indent=4)
#     with open("mihai.json", "w") as json_file:
#         json.dump(json_response, json_file, cls=ComplexEncoder, indent=2)
#     return json_str

@app.route('/simple_analyze/<statement>', methods=['GET'])
def simple_analyze(statement):
    print("Statement received")
    print(statement)
    my_statement = pb.Statement()
    my_statement.type = statement
    js_to_protobuf_queue.put(my_statement)
    print("... sent")
    print("wait_update")
    logging.warning("sending ...")
    logging.warning("wait_update ...")
    while True:
        try:
            logging.warning('A intrat in try')
            ret = protobuf_to_js_queue.get(block=True, timeout=1)
            logging.warning("GUI got update from protobuf! ...")
            print("GUI got update from protobuf!")
            logging.warning(ret)
            print(ret)
            break
        except queue.Empty:
            pass


    entities = grpc_message_to_dict(ret)
    logging.warning("dict format")
    print("dict format")
    print(entities)
    new_dic = {}
    for ent in entities['entities']:
        print(ent)
        print(ent['type'])
        print(ent['values'])
        new_dic[ent['type']] = ent['values']

    logging.warning("converted dict")
    print('converted dict')
    print(new_dic)

    json_str = json.dumps(new_dic, cls=ComplexEncoder, indent=4)
    return json_str

@app.route('/test', methods=['GET'])
def ok():
    logging.warning("Aici Test")
    return "ok"

@app.route('/', methods=['GET'])
def hello():
    logging.warning("Aici Main")
    return "Hello to Mindbugs Discovery. Try /simple_analyze/your Statement"


class MainKGImp(grcp_pb.MainKG):
    def __init__(self, to_protobuf_queue, to_js_queue):
        self.to_protobuf_queue = to_protobuf_queue
        self.to_js_queue = to_js_queue

    def RequestKeywords(self, request, context):
        logging.warning('Request key e chemat')
        print("Enters request keywords")
        try:
            while True:
                try:

                    # make sure we notice that the connection is gone if the orchestrator dies
                    ret = self.to_protobuf_queue.get(block=True, timeout=1.0)
                    print("received ret")
                    logging.warning("received ret")
                    logging.warning(ret)
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

    def ReceiveKeywords(self, request, context):
        logging.warning('Recive keywords')
        print("Enters receive keywords")
        logging.warning(request)
        print(request)
        self.to_js_queue.put(request)
        empty = pb.Empty()
        return empty



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

    app.run(host="0.0.0.0", port=8062, use_reloader=False)
    grpc_thread.join()
