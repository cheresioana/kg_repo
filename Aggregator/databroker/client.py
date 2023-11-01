import grpc
import time
import data_formats_pb2 as pb
import data_formats_pb2_grpc as grpc_pb

def run():
    # Initialize a channel and a stub (client)
    channel = grpc.insecure_channel('localhost:8061')  # Use the appropriate port number
    stub = grpc_pb.DataServiceStub(channel)

    while True:
        try:
            # Make a request to the server
            request = pb.Command()
            response = stub.GetData(request)
            print("Received:", response.statement, response.label)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                print("Server message:", e.details())
                break
            else:
                print("gRPC error:", e)
                break

if __name__ == '__main__':
    run()