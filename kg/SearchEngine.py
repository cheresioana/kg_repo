import itertools

import pandas as pd
import requests
from openai.embeddings_utils import cosine_similarity

from ChatGPT.OpenAIEmbeddingWrapper import OpenAIEmbeddingWrapper
from DataObject.SubGraphResult import SubGraphResult, Node, Link, SubGraph, ResultItem
from Neo4JConnector.NeoAlgorithms import NeoAlgorithms
from Neo4JConnector.NeoConnector import NeoConnector
from utils import clean_text


class SearchEngine():
    def __init__(self):
        self.embeddingWrapper = OpenAIEmbeddingWrapper()
        self.neo_connector = NeoConnector()
        self.neo_algo = NeoAlgorithms()

    def insert_query_elements(self, query):
        response = requests.post("http://127.0.0.1:5006/keywords", json={'statement': query})
        if response.status_code == 200:
            entities = response.json()
            query_node = self.neo_connector.insert_search_statement(query)
            self.neo_connector.insert_statement_entities(query_node.intra_id, entities)
            return query_node, entities
        return None

    def find_path_between_nodes(self, start, end):
        paths = self.neo_algo.find_dijkstra_path(start, end)
        return paths

    def parse_path(self, min_weight, path, query_id):
        nodes = []
        links = []
        # here if next paths in the graph are larger than the smallest do not take that option
        if path["weight"] > min_weight:
            return None, None
        index = 0
        previous_node = None
        for element in path['path']:
            if index % 2 == 0 and index > 0:
                # The node is of type tag
                if element.get('name') is not None:
                    new_node = Node(element["intra_id"], element["name"],
                                    element["intra_id"], tag="key_element")
                # the node is of type fake statement
                else:
                    new_node = Node(element["intra_id"], element["statement"],
                                    element["id"], tag="statement_node")
                nodes.append(new_node)
                # if there is a previous node add link between the current and previous
                if previous_node is not None:
                    links.append(Link(new_node.id, previous_node.id))
                # if there is not than that means it is connected to the origin
                else:
                    links.append(Link(new_node.id, query_id))
                previous_node = new_node
            index = index + 1
        return nodes, links
    def compute_paths(self, query_id, res_df):
        results = []
        for index, row in res_df.iterrows():
            paths = self.find_path_between_nodes(query_id, int(row["intra_id"]))
            location = self.neo_connector.get_statement_location(row["intra_id"])
            channel = self.neo_connector.get_statement_channel(row["intra_id"])
            min_weight = paths[0]["weight"]
            for path in paths:
                nodes, links = self.parse_path(min_weight, path, query_id)
                if nodes is not None:
                    results.append(ResultItem(paths[0]["weight"],
                                              row["intra_id"],
                                              query_id, row["statement"],
                                              nodes, links, date=row["date"],
                                              channel=channel, location=location))

        sorted_data = sorted(results, key=lambda x: x.weight)
        return sorted_data

    def find_results(self, query, query_node, query_entities):
        clean_query = clean_text(query)
        query_embedding = self.embeddingWrapper.get_embedding(clean_query)
        statements = self.neo_connector.get_statements_vectors()
        df = pd.DataFrame(statements)
        df["similarity"] = df['embedding'].apply(lambda x: cosine_similarity(x, query_embedding))
        results = (
            df.sort_values("similarity", ascending=False)
            .head(10)
        )

        #query_node, query_entities = self.insert_query_elements(query)

        if query_node is not None:
            path_result = self.compute_paths(query_node.intra_id, results)
            show_nodes = []
            show_links = []
            for index, row in results.head(3).iterrows():
                filtered_items = [item for item in path_result if item.intra_id == row["intra_id"]]
                for filtered_item in filtered_items:
                    filtered_item.selected = 1
                    show_nodes.extend(filtered_item.nodes)
                    show_links.extend(filtered_item.links)

            show_links = list(set(show_links))
            show_nodes = (list(set(show_nodes)))
            show_nodes.append(query_node)
            keywords = list(itertools.chain.from_iterable(query_entities.values()))

            return keywords, show_links, show_nodes, path_result, query_node

        return None
