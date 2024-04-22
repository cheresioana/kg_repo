import csv
import json
import os
from DataObject import DataObject
import pandas as pd
'''
This file represents the local state of the Scraper. It contains the links to the pages which were already 
scraped, in order not to duplicate values. 
'''
class LocalState:
    def __init__(self, db_filename='local_state.csv', faulty_filename='faulty.csv'):
        self.filename = db_filename
        self.faulty_filename = faulty_filename
        self.crawled_links = []
        data_obj_text = DataObject()
        self.field_names = list(data_obj_text.__dict__.keys())
        #sent items
        if os.path.exists(self.filename):
            data = pd.read_csv(self.filename, index_col=False)
            self.crawled_links = data['debunking_link'].tolist()
        else:
            with open(self.filename, 'a', encoding="utf-8") as f:
                dictwriter_object = csv.DictWriter(f, fieldnames=self.field_names)
                dictwriter_object.writeheader()
                f.close()
        #faulty items file
        self.faulty_fields = self.field_names
        self.faulty_links = []
        self.faulty_fields.append("manual_verification")
        if not os.path.exists(self.faulty_filename):
            with open(self.faulty_filename, 'a', encoding="utf-8") as f:
                dictwriter_object = csv.DictWriter(f, fieldnames=self.faulty_fields)
                dictwriter_object.writeheader()
                f.close()
        else:
            data = pd.read_csv(self.faulty_filename, index_col=False)
            self.faulty_links = data['debunking_link'].tolist()

    def append(self, obj):
        with open(self.filename, 'a', encoding="utf-8") as f:
            dictwriter_object = csv.DictWriter(f, fieldnames=self.field_names)
            dictwriter_object.writerow(obj.__dict__)
            f.close()

    def append_faulty(self, obj):
        obj.manual_verification = False
        print("Faulty: " + obj.statement)
        data = pd.read_csv(self.faulty_filename, index_col=False)
        df = data[data['debunking_link'] != obj.debunking_link]
        df.to_csv(self.faulty_filename, index=False)
        with open(self.faulty_filename, 'a', encoding="utf-8") as f:
            dictwriter_object = csv.DictWriter(f, fieldnames=self.faulty_fields)
            dictwriter_object.writerow(obj.__dict__)
            f.close()

    def get_faulty_df(self):
        data = pd.read_csv(self.faulty_filename, index_col=False)
        return data


    def already_parsed(self, link):
        return link in self.crawled_links

    def has_faulty(self, link):
        return link in self.faulty_links

    def remove_faulty(self, link):
        data = pd.read_csv(self.faulty_filename, index_col=False)
        df = data.drop(data[data['debunking_link'] == link].index)
        df.to_csv(self.faulty_filename, index=False)
        self.faulty_links.remove(link)

    def manual_verification(self, link):
        data = pd.read_csv(self.faulty_filename, index_col=False)
        element = data[data['debunking_link'] == link]
        element = element.fillna('')
        verification = element['manual_verification'].iloc[0]
        element = element.drop(['manual_verification'], axis=1)
        element = element.iloc[0]
        if verification == True:
            obj = DataObject()
            obj.init_from_df(element)
            return obj
        return None


    def add_crawled(self, link):
        self.crawled_links.append(link)
        #self.append(link)  # Add the link to the CSV file