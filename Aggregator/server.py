import logging

import grpc
from concurrent import futures
import data_formats_pb2 as pb
import data_formats_pb2_grpc as grcp_pb
from classifier.classifier import predict_statement, retrain_model
from knowledge_extraction.EntityExtractor import EntityExtractor

extractor = EntityExtractor()


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
    serve()
