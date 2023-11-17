import itertools

import pandas as pd
import re

from parsers.DataObject import DataObject


class BaseParser2:
    def __init__(self):
       pass

    @staticmethod
    def _get_next_id():
        try:
            with open('next_id.txt', 'r') as f:
                next_id = int(f.read())
        except FileNotFoundError:
            next_id = 0

        with open('next_id.txt', 'w') as f:
            f.write(str(next_id + 1))

        return next_id

    def parse(self, payload):
        data_object = DataObject()
        data_object.init_from_json(payload)
        return data_object.__dict__

