import logging
import threading

import grpc
from concurrent import futures
import data_formats_pb2 as pb
import data_formats_pb2_grpc as grcp_pb
from classifier.classifier import predict_statement, retrain_model
from knowledge_extraction.EntityExtractor import EntityExtractor
import pandas as pd
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

@app.route('/data', methods=['GET'])
def get_data():
    # Read the DataFrame from the CSV file
    try:
        df = pd.read_csv('local_data.csv')

        # Convert the DataFrame to a JSON object
        data_json = df.to_json(orient='records')
    except:
        data_json = "no data received yet"

    # Return the JSON response
    return jsonify(data_json)

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

    def ReceiveData(self, request, context):
        try:
            df = pd.read_csv("local_data.csv")
        except FileNotFoundError:
            df = pd.DataFrame(columns=["statement", "label"])
        new_data = pd.DataFrame({"statement": [request.statement], "label": [request.label]})
        df = pd.concat([df, new_data], ignore_index=True)
        # Write the updated DataFrame back to the CSV file.
        df.to_csv("local_data.csv", index=False)
        empty = pb.Empty()
        return empty



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
