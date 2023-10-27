import grpc
import model_pb2 as pb
import model_pb2_grpc as pb_grcp
from concurrent import futures
import logging
import sys
import time

g_1 = 0
g_2 = 0

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler(sys.stdout)])

class Client(pb_grcp.ClientService):
    def __init__(self):
        pass
    def RequestKeywords(self, request, context):
        global g_1
        request = pb.Statement()
        request.type = "Russia 100 euros Romania Ioana "
        logging.info("Here it enters in request keywords")
        if g_1 != 0:
            while g_1 != 0:
                time.sleep(20)
        else:
            g_1 = 1
        time.sleep(100)
        return request

    def ParseKeywords(self, request, context):
        global g_2
        logging.info("Here it enters in receive keywords")
        logging.info(request)

        response = request
        # Process the response here, e.g., print it
        for entity in response.entities:
            print(f"Entity Type: {entity.type}")
            print(f"Values: {entity.values}")
        if g_2 != 0:
            while g_2 != 0:
                time.sleep(20)
        else:
            g_2 = 1
        time.sleep(100)
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
