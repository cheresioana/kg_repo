import pandas as pd
import networkx as nx
import community  # python-louvain
import logging

# df = pd.read_csv("export.csv")
df = pd.read_csv("algo_community/export.csv")
G = nx.from_pandas_edgelist(df, source='source', target='target')


def find_community(closest_statement):
    logging.warning(f"Entering find community {closest_statement}")
    partition = community.best_partition(G)
    # Find the community of the closest_statement
    try:
        community_of_closest_statement = partition[closest_statement]

        # Print the community of the closest_statement
        logging.warning(
            f"The closest_statement '{closest_statement}' belongs to Community {community_of_closest_statement}")
        nodes_in_community = [node for node, community in partition.items() if
                              community == community_of_closest_statement]

        # Print the other statements and keywords in the same community
        return community_of_closest_statement, nodes_in_community
    except:
        logging.warning(f"Could not find the community of the closest statement")
        return -1, []


if __name__ == '__main__':
    closest_statement = "The West and Romania will enter the war on Ukraine"
    find_community(closest_statement)
