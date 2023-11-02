import grpc
from concurrent import futures
import time
import data_formats_pb2 as pb
import data_formats_pb2_grpc as grpc_pb
import pandas as pd

port = 8061


class Databroker(grpc_pb.DataService):

    def __init__(self):
        self.current_row = 0
        dataset = pd.read_csv("data_clean.csv")
        dataset = dataset.dropna(subset=['statement'])

        # If you want to reset the index after dropping rows, you can do the following:
        dataset.reset_index(drop=True, inplace=True)
        #dataset = dataset.dropna()
        self.dataset = dataset

    def GetData(self, request, context):
        response = pb.DataObject()
        print(self.dataset.shape)
        print(len(self.dataset))
        print(self.current_row)
        if self.current_row >= len(self.dataset):

            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("all data has been processed")
        else:
            response.statement = self.dataset.iloc[self.current_row]["statement"]
            response.label = self.dataset.iloc[self.current_row]["label"]
            self.current_row = self.current_row + 1

        return response


if __name__ == "__main__":
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    grpc_pb.add_DataServiceServicer_to_server(Databroker(), server)
    print("Starting server. Listening on port : " + str(port))
    server.add_insecure_port("[::]:{}".format(port))
    server.start()
    server.wait_for_termination()
