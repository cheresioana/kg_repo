import grpc
import data_formats_pb2 as pb
import data_formats_pb2_grpc as grcp_pb
import logging

def run_client():
    with grpc.insecure_channel('0.0.0.0:8061') as channel:
        while True:
            stub = grcp_pb.MainKGStub(channel)
            logging.info("Request keywords")
            request = pb.Empty()
            response = stub.RequestKeywords(request)
            print(response)
            with grpc.insecure_channel('0.0.0.0:8063') as channel2:  # Change the address/port if needed
                stub2 = grcp_pb.MainServiceStub(channel2)
                logging.info("Send request keywords to the aggregator")
                response2 = stub2.GetKeywords(response)
                print("received response from aggregator")
                print(response2)
            stub.ReceiveKeywords(response2)

def run_client2():
    channel = grpc.insecure_channel('0.0.0.0:8061')
    stub = grcp_pb.DataServiceStub(channel)
    channel2 = grpc.insecure_channel('0.0.0.0:8063')  # Change the address/port if needed
    stub2 = grcp_pb.MainServiceStub(channel2)
    while True:
      # Change the address/port if needed
        logging.info("call Add data")
        request = pb.Empty()
        response = stub.GetData(request)
        print(response)
        logging.info("Send data ")
        response2 = stub2.ReceiveData(response)
        print(response2)
        break


if __name__ == '__main__':
    run_client()
    #run_client2()