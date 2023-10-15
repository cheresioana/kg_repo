import csv
import json
import os

from parsers.BaseParser2 import BaseParser2


class LocalState:
    def __init__(self, db_filename='all_messages.json'):
        self.filename = db_filename

    def append_message(self, obj):
        with open(self.filename, 'r+', newline='', encoding="utf-8") as f:
            f.seek(os.stat(self.filename).st_size - 1)
            f.write(",{}]".format(obj, indent=4))

    def save_parsed_entry(self, entry , csv_filename="data2.csv"):
        if not os.path.isfile(csv_filename):
            with open(csv_filename, 'w', newline='') as csvfile:
                headers = list(entry.keys())
                #print(f'Headers: {headers}')
                writer = csv.writer(csvfile)
                writer.writerow(headers)
                writer.writerow(list(entry.values()))
        else:
            with open(csv_filename, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                #print(f'Headers: {list(entry.final_object.values())}')
                writer.writerow(list(entry.values()))
