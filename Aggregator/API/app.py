import os
import sys

from flask import Flask, jsonify, request
import json
from flask_cors import CORS
import data_formats_pb2 as pb
from data_formats_pb2 import Statement as statement
from flask_protobuf import flask_protobuf as FlaskProtobuf

sys.path.append(os.path.dirname(os.path.abspath('/home/ioana/kg_repo/Aggregator/knowledge_extraction')))
from knowledge_extraction.EntityExtractor import EntityExtractor

app = Flask(__name__)
fb = FlaskProtobuf(app, parse_dict=True)
extractor = EntityExtractor()
CORS(app)


# Sample data
# def load_kg():
#     with open('../kg.json', 'r') as file:
#         data = json.load(file)
#         file.close()
#     return data
#
#
# @app.route('/kg', methods=['GET'])
# def get_kg():
#     nodes = load_kg()
#     return jsonify(nodes)
#
#
@app.route('/keywords', methods=['POST'])
@fb(statement, parse_dict=True)
def get_keywords():
    print(request.data)
    data = request.data
    print(data)
    print(data['type'])
    entities = extractor.extract_entities(data['type'])
    print(entities)
    ent_response = pb.EntityResponse()
    my_arr = []
    for key in entities:
        ent_obj = pb.Entity()
        ent_obj.type=key
        print(entities[key])
        ent_obj.values.extend(entities[key])
        my_arr.append(ent_obj)
    ent_response.entities.extend(my_arr)
    response_data = ent_response.SerializeToString()
    print(response_data)
    return response_data, 200, {'Content-Type': 'application/x-protobuf'}

    #return jsonify(entities)


# @app.route('/keywords2', methods=['POST'])
# @fb(keywords2, parse_dict=True)
# def get_keywords2():
#     print("WTF")
#     request_data = request.data
#     request_proto = pb.Statement()
#     request_proto.ParseFromString(request_data)
#     print(request_proto.type)
#
#     entities = extractor.extract_entities(request_proto.type)
#     print(entities)
#     ent_response = pb.EntityResponse()
#     my_arr = []
#     for key in entities:
#         ent_obj = pb.Entity()
#         ent_obj.type=key
#         ent_obj.values=entities[key]
#         my_arr.append(ent_obj)
#     ent_response.entities = my_arr
#     response_data = ent_response.SerializeToString()
#     print(response_data)
#     return response_data, 200, {'Content-Type': 'application/x-protobuf'}



if __name__ == '__main__':
    app.run()
