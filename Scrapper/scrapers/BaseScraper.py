import json
from abc import abstractmethod

import DataObject
from LocalState import LocalState
from QueueConnectionModule import QueueConnectionModule


class BaseScraper:
    def __init__(self, db_filename, faulty_filename):
        """
        Save the local state and the queue connection modules
        """
        self.local_state = LocalState(db_filename, faulty_filename)
        self.queue = QueueConnectionModule()

    @abstractmethod
    def complete_info(self, data_obj: DataObject):
        """
        This abstract function is implemented in each class and decides if the dataobject scraped is complete
        :param data_obj: data scraped
        :return: True or False depending for each scraper what means a complete data object
        """
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

    def manual_inputted_data(self, debunking_link, rescrape_faulty):
        """
        If manual inputed data is found, then it just reads from the faulty csv and sends it directly to the aggregator
        :param debunking_link rescrape_faulty:
        :return: True (manual data is found), False (no manual data was found)
        """
        element = self.local_state.manual_verification(debunking_link)
        if element is not None:
            self.send_data(element, rescrape_faulty)
            return True
        return False

