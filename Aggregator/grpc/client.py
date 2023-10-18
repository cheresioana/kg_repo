import grpc
import data_formats_client_pb2 as pb
import data_formats_client_pb2_grpc as pb_grcp
from concurrent import futures


class Client(pb_grcp.ClientService):
    def RequestKeywords(self, request, context):
        request = pb.Statement()
        request.type = "Russia 100 euros Romania Ioana "
        print("Here it enters in request keywords")
        return request

    def ParseKeywords(self, request, context):
        print("Here it enters in receive keywords")
        print(request)
        response = request
        # Process the response here, e.g., print it
        for entity in response.entities:
            print(f"Entity Type: {entity.type}")
            print(f"Values: {entity.values}")
        return pb.Empty()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb_grcp.add_ClientServiceServicer_to_server(Client(), server)
    server.add_insecure_port('[::]:8061')  # Change the port if needed
    server.start()
    print("Started server")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
