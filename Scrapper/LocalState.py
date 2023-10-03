import csv
import json
import os
from DataObject import DataObject

'''
This file represents the local state of the Scraper. It contains the links to the pages which were already 
scraped, in order not to duplicate values. 
'''
class LocalState:
    def __init__(self, db_filename='local_state.json'):
        self.filename = db_filename
        self.crawled_links = []
        with open(self.filename, "r") as f:
            try:
                json_data = json.load(f)
            except:
                json_data = []
        attribute_name = "debunking_link"
        for item in json_data:
            if attribute_name in item:
                self.crawled_links.append(item[attribute_name])

    def append(self, obj: DataObject):

        with open(self.filename, 'r+', newline='', encoding="utf-8") as f:
            file_size = os.stat(self.filename).st_size
            if file_size > 0:
                f.seek(file_size - 1)
                f.write(",{}]".format(json.dumps(obj.json_encoder(), indent=4)))
            else:
                f.write("[{}]".format(json.dumps(obj.json_encoder(), indent=4)))

    def already_parsed(self, link):
        if link in self.crawled_links:
            return True
        return False

    def add_crawled(self, link):
        self.crawled_links.append(link)