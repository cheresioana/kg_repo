import grpc
import data_formats_pb2 as pb
import data_formats_pb2_grpc as grcp_pb


def run_client():
    with grpc.insecure_channel('0.0.0.0:8063') as channel:  # Change the address/port if needed
        stub = grcp_pb.MainServiceStub(channel)

        # Prepare a request
        request = pb.Statement()
        request.type = "Russia 100 euros Romania Ioana "

        # Make 10 requests
        for _ in range(10):
            response = stub.GetKeywords(request)

            # Process the response here, e.g., print it
            for entity in response.entities:
                print(f"Entity Type: {entity.type}")
                print(f"Values: {entity.values}")


if __name__ == '__main__':
    run_client()