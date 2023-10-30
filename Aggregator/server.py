import logging
import threading

import grpc
from concurrent import futures
import data_formats_pb2 as pb
import data_formats_pb2_grpc as grcp_pb
from classifier.classifier import predict_statement, retrain_model
from knowledge_extraction.EntityExtractor import EntityExtractor

from flask import Flask, jsonify, request
import json
from flask_cors import CORS

extractor = EntityExtractor()

app = Flask(__name__)

CORS(app)


@app.route('/retrain', methods=['GET'])
def retrain():
    acc = retrain_model()
    return str(acc)

@app.route('/', methods=['GET'])
def hello():
    logging.warning("Aici Main AGG")
    return "this is aggregator. Try /retrain"


class Main(grcp_pb.MainService):
    def __int__(self):
        pass

    def GetKeywords(self, request, context):
        logging.warning("Suntem in get keyords aggregator")
        data_type = request.type
        entities = extractor.extract_entities(data_type)
        logging.warning("entities")
        logging.warning(entities)
        response = pb.EntityResponse()
        for key, values in entities.items():
            logging.warning('key')
            logging.warning(key)
            logging.warning('values')
            logging.warning(values)
            entity = pb.Entity()
            entity.type = key
            entity.values.extend(values)
            response.entities.append(entity)
        response.label = predict_statement(data_type)
        return response

    def RetrainModel(self, request, context):
        acc = retrain_model()
        accuracy = pb.Accuracy()
        accuracy.acc = acc
        return accuracy



def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    grcp_pb.add_MainServiceServicer_to_server(Main(), server)
    server.add_insecure_port('[::]:8061')  # Change the port if needed
    server.start()
    print("Started server")
    server.wait_for_termination()


if __name__ == '__main__':
    grpc_thread = threading.Thread(target=serve)
    print("Started server")
    grpc_thread.start()

    app.run(host="0.0.0.0", port=8062, use_reloader=False)
    grpc_thread.join()
