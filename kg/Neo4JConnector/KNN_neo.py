import os
from graphdatascience import GraphDataScience
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from constanst import NEO4J_URI, NEO4J_AUTH

if __name__ == '__main__':


    gds = GraphDataScience(NEO4J_URI, auth=NEO4J_AUTH)
    gds.set_database("neo4j")

    node_projection = ["Person", "Fake_Statement", "Entity"]
    relationship_projection = {"HAS_KEYWORD": {"orientation": "UNDIRECTED"}}
    result = gds.graph.project.estimate(node_projection, relationship_projection)
    print(f"Required memory for native loading: {result['requiredMemory']}")
    G = gds.graph.get("purchases")
    gds.graph.drop(G, False)
    G, result = gds.graph.project("purchases", node_projection, relationship_projection)
    print(f"The projection took {result['projectMillis']} ms")

    result = gds.fastRP.mutate.estimate(
        G,
        mutateProperty="embedding",
        randomSeed=42,
        embeddingDimension=4,
        iterationWeights=[0.8, 1, 1, 1],
    )

    print(f"Required memory for running FastRP: {result['requiredMemory']}")
    # Now let's run FastRP and mutate our projected graph 'purchases' with the results
    result = gds.fastRP.mutate(
        G,
        mutateProperty="embedding",
        randomSeed=42,
        embeddingDimension=4,
        iterationWeights=[0.8, 1, 1, 1],
    )

    # Let's make sure we got an embedding for each node
    print(f"Number of embedding vectors produced: {result['nodePropertiesWritten']}")

    result = gds.knn.write(
        G,
        topK=2,
        nodeProperties=["embedding"],
        randomSeed=42,
        concurrency=1,
        sampleRate=1.0,
        deltaThreshold=0.0,
        writeRelationshipType="SIMILAR",
        writeProperty="score",
    )

    print(f"Relationships produced: {result['relationshipsWritten']}")
    print(f"Nodes compared: {result['nodesCompared']}")
    print(f"Mean similarity: {result['similarityDistribution']['mean']}")

