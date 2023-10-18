import grpc
import data_formats_client_pb2 as pb
import data_formats_client_pb2_grpc as pb_grcp


class ClientApp:
    def __init__(self, channel):
        self.stub = pb_grcp.ClientServiceStub(channel)

    def request_keywords(self):
        # Call the RequestKeywords RPC method
        empty_request = pb.Empty()
        response = self.stub.RequestKeywords(empty_request)
        print(f"Received statement: {response.type}")

    def send_keywords_for_parsing(self):
        # Sample data to send (just for demonstration)
        entities = []
        ent1 = pb.Entity()
        ent1.type = "Country"
        ent1.values.append("Russia")
        ent1.values.append("Romania")
        entities.append(ent1)
        entity_response = pb.EntityResponse()

        entity_response.entities.extend(entities)
        print(entity_response)

        response = self.stub.ParseKeywords(entity_response)
        print("Keywords sent for parsing")


if __name__ == "__main__":
    with grpc.insecure_channel('localhost:8061') as channel:
        client = ClientApp(channel)
        client.request_keywords()
        client.send_keywords_for_parsing()
