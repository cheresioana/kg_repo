import json
from abc import abstractmethod

import DataObject
from LocalState import LocalState
from QueueConnectionModule import QueueConnectionModule


class BaseScraper:
    def __init__(self, db_filename, faulty_filename):
        self.local_state = LocalState(db_filename, faulty_filename)
        self.queue = QueueConnectionModule()

    @abstractmethod
    def complete_info(self, data_obj: DataObject):
        pass

    def send_data(self, data_object, rescrape_faulty):
        """
        sends data through RMQ to the aggregator component
        """
        print(f'Sent data: {data_object.statement}')
        self.local_state.append(data_object)
        self.queue.send_message(json.dumps(data_object.json_encoder()))
        if rescrape_faulty:
            self.local_state.remove_faulty(data_object.debunking_link)

