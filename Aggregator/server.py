import grpc
from concurrent import futures
import data_formats_pb2 as pb
import data_formats_pb2_grpc as grcp_pb
from knowledge_extraction.EntityExtractor import EntityExtractor

extractor = EntityExtractor()


class Main(grcp_pb.MainService):
    def GetKeywords(self, request, context):
        data_type = request.type
        entities = extractor.extract_entities(data_type)

        response = pb.EntityResponse()
        for key, values in entities.items():
            entity = pb.Entity()
            entity.type = key
            entity.values.extend(values)
            response.entities.append(entity)

        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    grcp_pb.add_MainServiceServicer_to_server(Main(), server)
    server.add_insecure_port('[::]:8061')  # Change the port if needed
    server.start()
    print("Started server")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
