import grpc
import data_formats_pb2 as pb
import data_formats_pb2_grpc as grcp_pb
import logging

def run_client():
    with grpc.insecure_channel('0.0.0.0:8061') as channel:  # Change the address/port if needed
        stub = grcp_pb.MainKGStub(channel)
        logging.info("Request keywords")
        request = pb.Empty()
        response = stub.RequestKeywords(request)
        print(response)


if __name__ == '__main__':
    run_client()