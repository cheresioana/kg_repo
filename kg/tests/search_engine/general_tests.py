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


class TestBasicFunctions(unittest.TestCase):

    def test_clean_text(self):
        result = clean_text("In 2021 the zombie apocalypse comes, but humanity will be saved by robot people and the church")
        self.assertEqual("2021 zombi apocalyps comes, human save robot peopl church", result)

    def test_search(self):
        query = "Transylvania is going to be sold to the EU"

        df = pd.read_csv('data/data_with_embeddings.csv')
        df["embedding"] = df["embedding"].apply(literal_eval).apply(np.array)
        embeddingWrapper = OpenAIEmbeddingWrapper()
        results = embeddingWrapper.search_vector_space_dataframe(df, query, n=5)
        print(f'Querry: {query}')
        for index,result in results.iterrows():
            print(result["statement"])
            print(result["fake_news_content"])
            print()
            print()

    def test_search2(self):
        query = "The war saved Russia from unemployment and poverty"

        df = pd.read_csv('data/data_with_embeddings.csv')
        df["embedding"] = df["embedding"].apply(literal_eval).apply(np.array)
        embeddingWrapper = OpenAIEmbeddingWrapper()
        results = embeddingWrapper.search_vector_space_dataframe(df, query, n=5)
        print(f'Querry: {query}')
        for index, result in results.iterrows():
            print(result["statement"])
            print(result["fake_news_content"])
            print()
        self.assertEqual("The war saved Russia from unemployment and poverty", results.iloc[0]["statement"])

    def test_search3(self):
        query = "The West pushes Moldova to go on the path of Ukraine"

        df = pd.read_csv('data/data_with_embeddings.csv')
        df["embedding"] = df["embedding"].apply(literal_eval).apply(np.array)
        embeddingWrapper = OpenAIEmbeddingWrapper()
        results = embeddingWrapper.search_vector_space_dataframe(df, query, n=5)
        print(f'Querry: {query}')
        for index, result in results.iterrows():
            print(result["statement"])
            print(result["fake_news_content"])
            print()
        self.assertEqual("The West forces Moldova to follow the path of Ukraine", results.iloc[0]["statement"])

    def test_search4(self):
        query = "The US will send 200 thousand Ukrainian military"

        df = pd.read_csv('data/data_with_embeddings.csv')
        df["embedding"] = df["embedding"].apply(literal_eval).apply(np.array)
        embeddingWrapper = OpenAIEmbeddingWrapper()
        results = embeddingWrapper.search_vector_space_dataframe(df, query, n=5)
        for index, result in results.iterrows():
            print(result["statement"])
            print(result["fake_news_content"])
            print()
        self.assertEqual("The US will send 200 thousand Ukrainian military-sugargias, subordinated directly to the Pentagon", results.iloc[0]["statement"])

    def test_get_statement_vectors1(self):
        neo_connector = NeoConnector()
        statements = neo_connector.get_statements_vectors()
        len_statements = len(statements)
        df = pd.DataFrame(statements)

        self.assertEqual(['id', 'intra_id', 'embedding', 'statement'], list(df.columns))
        self.assertEqual((len_statements, 4), df.shape)

    def test_search_engine1(self):
        search_engine = SearchEngine()
        subgraph_results = search_engine.find_results("The US will send 200 thousand Ukrainian military")
        # self.assertEqual("The US will send 200 thousand Ukrainian military-sugargias, subordinated directly to the "
        #                  "Pentagon", results[0]["statement"])

    def test_insert_query1(self):
        search_engine = SearchEngine()
        results = search_engine.insert_query_elements("The US will send 200 thousand Ukrainian military")

    def test_remove_query1(self):
        neo_connector = NeoConnector()
        neo_connector.drop_fake_statements_associates(657)

    def test_find_path_between(self):
        neo_algo = NeoAlgorithms()
        paths = neo_algo.find_dijkstra_path(178, 25)
        for path in paths:
            self.assertEqual(2, path['weight'])

    def test_get_statement_location(self):
        neo_connector = NeoConnector()
        location = neo_connector.get_statement_location(566)
        self.assertEqual(1, len(location))
        self.assertEqual("Romania", location[0])

    def test_get_statement_channel(self):
        neo_connector = NeoConnector()
        location = neo_connector.get_statement_channel(114)
        self.assertEqual(1, len(location))
        self.assertEqual("ukraina.ru", location[0])

if __name__ == '__main__':
    unittest.main()
