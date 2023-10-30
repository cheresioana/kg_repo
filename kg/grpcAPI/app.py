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
from flask import Flask, jsonify, request, render_template
import json
from flask_cors import CORS
import requests
from Neo4JConnector.NeoConnector import (NeoConnector)
from ChatGPT.ChatGPTWrapper import ChatGPTWrapper
from Neo4JConnector.NeoAlgorithms import (NeoAlgorithms)
import pandas as pd
import logging

app = Flask(__name__)

CORS(app)


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


@app.route('/simple_analyze/', methods=['GET'])
def simple_analyze():
    statement = request.args.get('statement')
    if not statement:
        return "No statement Provided"
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
    new_dic['label'] = entities["label"]
    logging.warning("converted dict")
    print('converted dict')
    print(new_dic)

    json_str = json.dumps(new_dic, cls=ComplexEncoder, indent=4)
    return json_str


@app.route('/retrain', methods=['GET'])
def retrain():
    my_commnad = pb.Command()
    js_to_protobuf_queue2.put(my_commnad)
    print("... sent")
    print("wait_update")
    logging.warning("sending ...")
    logging.warning("wait_update ...")
    while True:
        try:
            logging.warning('A intrat in try')
            ret = protobuf_to_js_queue2.get(block=True, timeout=1)
            logging.warning("GUI got update from protobuf! ...")
            print("GUI got update from protobuf!")
            logging.warning(ret)
            print(ret)
            break
        except queue.Empty:
            pass

    return "Accuracy: " + str(ret.acc)


@app.route('/test', methods=['GET'])
def ok():
    logging.warning("Aici Test")
    return "ok"


@app.route('/', methods=['GET'])
def hello():
    logging.warning("Aici Main")
    return render_template('index.html')


class MainKGImp(grcp_pb.MainKG):
    def __init__(self, to_protobuf_queue, to_js_queue, to_protobuf_queue2, to_js_queue2):
        self.to_protobuf_queue = to_protobuf_queue
        self.to_js_queue = to_js_queue
        self.to_protobuf_queue2 = to_protobuf_queue2
        self.to_js_queue2 = to_js_queue2

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

    def RequestTrain(self, request, context):
        logging.warning('Request train e chemat')
        print("Enters request train")
        try:
            while True:
                try:

                    # make sure we notice that the connection is gone if the orchestrator dies
                    ret = self.to_protobuf_queue2.get(block=True, timeout=1.0)
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

    def ReceiveAcc(self, request, context):
        logging.warning('Recive train')
        print("Enters receive keywords")
        logging.warning(request)
        print(request)
        self.to_js_queue2.put(request)
        empty = pb.Empty()
        return empty

    '''
     rpc RequestTrain(Empty) returns (Command);
      rpc ReceiveAcc(Accuracy) returns (Empty);
    '''


protobuf_to_js_queue = queue.Queue()
js_to_protobuf_queue = queue.Queue()

protobuf_to_js_queue2 = queue.Queue()
js_to_protobuf_queue2 = queue.Queue()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    grcp_pb.add_MainKGServicer_to_server(
        MainKGImp(js_to_protobuf_queue, protobuf_to_js_queue, js_to_protobuf_queue2, protobuf_to_js_queue2), server)
    server.add_insecure_port('[::]:8061')  # Change the port if needed
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    grpc_thread = threading.Thread(target=serve)
    print("Started server")
    grpc_thread.start()

    app.run(host="0.0.0.0", port=8062, use_reloader=False)
    grpc_thread.join()
