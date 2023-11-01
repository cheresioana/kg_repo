import ast
import sys
import os
import threading
import traceback
import time
import queue
from openai.embeddings_utils import cosine_similarity
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ChatGPT.OpenAIEmbeddingWrapper import OpenAIEmbeddingWrapper
from utils import clean_text
from DataObject.SubGraphResult import ComplexEncoder, ResultItem, Node, Link
try:
    from _queue import SimpleQueue
except ImportError:
    SimpleQueue = None
import grpc
from concurrent import futures
import data_formats_pb2 as pb
import data_formats_pb2_grpc as grcp_pb
from flask import Flask, jsonify, request, render_template
import json
from flask_cors import CORS
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

embeddingWrapper = OpenAIEmbeddingWrapper()
df = pd.read_csv("data/data_with_embeddings.csv")
df = df[["statement", "embedding"]]
df = df.dropna()
df['embedding'] = df['embedding'].apply(lambda x: [float(i) for i in ast.literal_eval(x)])

@app.route('/simple_analyze/', methods=['GET'])
def simple_analyze():
    statement = request.args.get('statement')
    if not statement:
        return "No statement Provided"
    my_statement = pb.Statement()
    my_statement.type = statement
    js_to_protobuf_queue.put(my_statement)
    logging.warning("sending ...")
    logging.warning("wait_update ...")
    while True:
        try:
            logging.warning('A intrat in try')
            ret = protobuf_to_js_queue.get(block=True, timeout=1)
            logging.warning("GUI got update from protobuf! ...")
            logging.warning(ret)
            break
        except queue.Empty:
            pass

    entities = grpc_message_to_dict(ret)
    logging.warning("dict format")
    new_dic = {}
    for ent in entities['entities']:
        new_dic[ent['type']] = ent['values']
    new_dic['label'] = entities["label"]
    logging.warning("converted dict")
    logging.warning("clean query")
    clean_query = clean_text(statement)
    logging.warning("Query embedding")
    query_embedding = embeddingWrapper.get_embedding(clean_query)
    logging.warning("similarity")
    df["similarity"] = df['embedding'].apply(lambda x: cosine_similarity(x, query_embedding))
    logging.warning(df.shape)
    results = (
        df.sort_values("similarity", ascending=False)
        .head(5)
    )
    logging.warning(results)
    new_dic['statements'] = results['statement'].tolist()

    json_str = json.dumps(new_dic, cls=ComplexEncoder, indent=4)
    return json_str




@app.route('/test', methods=['GET'])
def ok():
    logging.warning("Aici Test")
    return "ok"


@app.route('/', methods=['GET'])
def hello():
    logging.warning("Aici Main")
    return render_template('index.html')


class MainKGImp(grcp_pb.MainKG):
    def __init__(self, to_protobuf_queue, to_js_queue):
        self.to_protobuf_queue = to_protobuf_queue
        self.to_js_queue = to_js_queue


    def RequestKeywords(self, request, context):
        logging.warning('Request key is called')
        try:
            while True:
                try:
                    # make sure we notice that the connection is gone if the orchestrator dies
                    ret = self.to_protobuf_queue.get(block=True, timeout=1.0)
                    logging.warning("received ret")
                    logging.warning(ret)
                    return ret
                except queue.Empty:
                    if not context.is_active():
                        raise RuntimeError("RPC interrupted - leaving requestSudokuEvaluation")
                    # otherwise continue
        except Exception:
            time.sleep(1)
            pass

    def ReceiveKeywords(self, request, context):
        logging.warning('Recive keywords')
        logging.warning(request)
        self.to_js_queue.put(request)
        empty = pb.Empty()
        return empty


protobuf_to_js_queue = queue.Queue()
js_to_protobuf_queue = queue.Queue()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    grcp_pb.add_MainKGServicer_to_server(
        MainKGImp(js_to_protobuf_queue, protobuf_to_js_queue), server)
    server.add_insecure_port('[::]:8061')  # Change the port if needed
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    grpc_thread = threading.Thread(target=serve)
    logging.warning("started server")
    grpc_thread.start()
    app.run(host="0.0.0.0", port=8062, use_reloader=False)
    grpc_thread.join()
