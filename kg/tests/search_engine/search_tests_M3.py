import time
import unittest
import os
from ast import literal_eval
import numpy as np

import openai
from openai.embeddings_utils import get_embedding
import pandas as pd

from ChatGPT.OpenAIEmbeddingWrapper import OpenAIEmbeddingWrapper
from Neo4JConnector.NeoAlgorithms import NeoAlgorithms
from Neo4JConnector.NeoConnector import NeoConnector
from SearchEngine import SearchEngine
from utils import clean_text


class SearchTestsM3(unittest.TestCase):


    def test_search1(self):
        search_engine = SearchEngine()
        query = "Joe Biden"
        start_time = time.time()
        keywords, show_links, show_nodes, path_result, origin_node = search_engine.find_results(query)
        duration = time.time() - start_time
        print(f"The Unit test took {duration} seconds to run.")
        self.assertLess(1, 30)

    def test_search2(self):
        search_engine = SearchEngine()
        query = "EU is forcing people to eat insects"
        start_time = time.time()
        keywords, show_links, show_nodes, path_result, origin_node = search_engine.find_results(query)
        duration = time.time() - start_time
        print(f"The Unit test took {duration} seconds to run.")
        self.assertLess(1, 30)

    def test_search3(self):
        search_engine = SearchEngine()
        query = "USA is evil"
        start_time = time.time()
        keywords, show_links, show_nodes, path_result, origin_node = search_engine.find_results(query)
        duration = time.time() - start_time
        print(f"The Unit test took {duration} seconds to run.")
        self.assertLess(1, 30)

if __name__ == '__main__':
    unittest.main()
