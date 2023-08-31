import os
import sys
import pandas as pd
import random
from sklearn.metrics import accuracy_score
from graphdatascience import GraphDataScience
from collections import Counter
import spacy
import pytextrank
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


NEO4J_URI = "bolt://localhost:7687"

NEO4J_AUTH = ('neo4j', 'ioana123')
sys.path.append(os.path.dirname(os.path.abspath('/home/ioana/kg_repo/kg/Neo4JConnector')))

from Neo4JConnector.NeoAlgorithms import (NeoAlgorithms)
from Neo4JConnector.NeoConnector import (NeoConnector)


def get_simple_keywords(row):
    #ents = title_entities.values()
    #ents = [item for sublist in ents for item in sublist]
    entities = {}
    # print(ents)
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("textrank")
    my_text = ''
    if not pd.isna(row['statement']):
        my_text = row['statement']

    if not pd.isna(row['fake_news_content']):
        my_text =  my_text + row['fake_news_content']
    processed = nlp(my_text)
    keywords = [p.text for p in processed._.phrases]

    # print(keywords)

    result = [item for item in keywords]
    # print(result)
    result2 = []
    nlp2 = spacy.load("en_core_web_sm")
    index = 0
    for text in result:
        word_tokens = word_tokenize(text)

        # Define stopwords
        stop_words = set(stopwords.words('english'))

        # Filter out the stopwords
        filtered_text = [word for word in word_tokens if not word in stop_words]

        # Convert list of words back to string
        filtered_text = ' '.join(filtered_text)
        if len(filtered_text) < 4:
            continue

        processed = nlp2(filtered_text)
        for en in processed.ents:
            if en.label_ not in entities:
                entities[en.label_] = list()
            entities[en.label_].append(en.text.replace("\'s", "").strip())
        if not processed.ents:
            if 'simple_keyword' not in entities:
                entities['simple_keyword'] = []
            entities['simple_keyword'].append(filtered_text)
        index = index + 1
        if index > 6:
            break
        # result2.append(filtered_text)

    return entities

def knn():
    gds = GraphDataScience(NEO4J_URI, auth=NEO4J_AUTH)
    gds.set_database("news")

    node_projection = ["Person", "Fake_Statement", "Entity"]
    relationship_projection = {"HAS_KEYWORD": {"orientation": "UNDIRECTED"}}
    result = gds.graph.project.estimate(node_projection, relationship_projection)
    #print(f"Required memory for native loading: {result['requiredMemory']}")
    try:
        G = gds.graph.get("purchases")
        gds.graph.drop(G, False)
    except:
        print("No previous projection found")
        pass
    G, result = gds.graph.project("purchases", node_projection, relationship_projection)
    #print(f"The projection took {result['projectMillis']} ms")

    # result = gds.fastRP.mutate.estimate(
    #     G,
    #     mutateProperty="embedding",
    #     randomSeed=42,
    #     embeddingDimension=4,
    #     iterationWeights=[0.8, 1, 1, 1],
    # )
    #
    # print(f"Required memory for running FastRP: {result['requiredMemory']}")
    # Now let's run FastRP and mutate our projected graph 'purchases' with the results
    result = gds.fastRP.mutate(
        G,
        mutateProperty="embedding",
        randomSeed=42,
        embeddingDimension=256,
        iterationWeights=[0.8, 1, 1],
    )

    print("FastRP time: " + str(result['computeMillis']))

    # Let's make sure we got an embedding for each node
    #print(f"Number of embedding vectors produced: {result['nodePropertiesWritten']}")

    result = gds.knn.write(
        G,
        topK=5,
        nodeProperties=["embedding"],
        randomSeed=1337,
        concurrency=1,
        sampleRate=1.0,
        deltaThreshold=0.0,
        writeRelationshipType="SIMILAR",
        writeProperty="score",
    )

    print("KNN time: " + str(result['computeMillis']))

    #print(f"Relationships produced: {result['relationshipsWritten']}")
    #print(f"Nodes compared: {result['nodesCompared']}")
    #print(f"Mean similarity: {result['similarityDistribution']['mean']}")


def compute_communities():
    neo = NeoAlgorithms()
    neo.run_louvain()


def drop_random():
    neo = NeoConnector()
    communities = neo.get_communities()
    dropped = []
    for community in communities:
        if community['Fake_S'] > 10:
            random_items = random.sample(community['statements'], 3)
            #random_items = community['statements'][:3]
            for item in random_items:
                neo.drop_fake_statements_associates(item['id'])
            dropped.extend(random_items)
            #return dropped
    return dropped


def evaluate_insert(elements):
    df = pd.read_csv('../../data.csv', index_col=None)
    connector = NeoConnector()
    connector.del_similar_rel()
    neo = NeoAlgorithms()
    #connector.drop_fake_statements_associates(3194)
    for element in elements:
        row = df[df['id'] == element['id']].iloc[0]
        title_entities = eval(row['title_entities'])
        keywords = eval(row['keywords'])
        connector.insert_statement(row)
        connector.insert_statement_entities(row['id'], get_simple_keywords(row))
        connector.insert_statement_entities(row['id'], title_entities)
        #connector.insert_statement_entities(row['id'], keywords)

    knn()
    final_communities = []
    baseline = []
    for element in elements:
        print(element)
        res = neo.find_similar(element['id'])
        selected_communities = [r['community'] for r in res]
        selected_communities = list(filter(lambda x: x is not None, selected_communities))
        counter = Counter(selected_communities)
        # print(counter.most_common(1)[0][0])
        print(selected_communities)

        if len(selected_communities) == 0:
            final_communities.append(-1)
        else:
            final_communities.append(counter.most_common(1)[0][0])

        baseline_res = neo.find_similar_baseline(element['id'])
        baseline_communities = baseline_res[0]['communities']
        baseline_communities = list(filter(lambda x: x is not None, baseline_communities))
        counter = Counter(baseline_communities)

        if len(baseline_communities) == 0:
            baseline.append(-1)
        else:
            baseline.append(counter.most_common(1)[0][0])
            print(counter.most_common(1)[0][0])

        # for r in res:
        #     print(f'{r["community"]}: {r["statement"]}')
        print('__________________________')
    real_communities = [element["community"] for element in elements]
    print(real_communities)
    print(final_communities)
    print(baseline)
    accuracy = accuracy_score(real_communities, final_communities)
    print(f'Accuracy: {accuracy}')
    accuracy = accuracy_score(real_communities, baseline)
    print(f'Baseline accuracy: {accuracy}')


if __name__ == "__main__":
    compute_communities()
    #exit(0)
    elements = drop_random()
    print(elements)

    # elements = [
    #     {
    #         'statement': 'A Russian official demands the "denazification" of the Baltic states, Poland, the Republic of Moldova and Kazakhstan',
    #         'id': 3194, 'community': 2102},
    #     {
    #         'statement': "Because of Kiev's neo-Nazi propaganda, Ukrainians do not understand that they are liberated from Russia, not occupied",
    #         'id': 3085, 'community': 2102},
    #     {'statement': 'The US allowed Ukraine to bomb Russia', 'id': 2936, 'community': 2102}
    # ]
    evaluate_insert(elements)
    # neo = NeoAlgorithms()
    # connector = NeoConnector()
    # connector.del_similar_rel()
    # knn()
    # print(neo.find_similar(3194))
