from Neo4JConnector.NeoConnector import NeoConnector

NEO4J_URI = "bolt://localhost:7687"

NEO4J_AUTH = ('neo4j', 'ioana123')
from graphdatascience import GraphDataScience
class NeoAlgorithms(NeoConnector):
    def run_louvain(self):
        DROP_IF_EXISTS = '''
        USE news
        CALL gds.graph.drop('myGraph', false) YIELD graphName;
        '''
        with self.driver.session() as session:
            records, summary, keys = self.driver.execute_query(DROP_IF_EXISTS)

        CREATE_PROJECTION_QUERY = '''
        USE news
        CALL gds.graph.project(
        'myGraph',
        ['Fake_Statement', 'Entity', 'Person'],
        {
            HAS_KEYWORD: {
                orientation: 'UNDIRECTED'
            }
        }
        )'''
        with self.driver.session() as session:
            records, summary, keys = self.driver.execute_query(CREATE_PROJECTION_QUERY)


        WRITE_COMMUNITY = '''
        USE news
        CALL gds.louvain.write('myGraph', { writeProperty: 'community' })
        YIELD communityCount, modularity, modularities
        '''
        with self.driver.session() as session:
            records, summary, keys = self.driver.execute_query(WRITE_COMMUNITY)
            avail = summary.result_available_after
            cons = summary.result_consumed_after
            total_time = avail + cons
            print("Louvain time: " + str(total_time))
            
    def find_dijkstra_path(self, start_id, end_id):
        FIND_PATH = '''
            USE news
            MATCH (a:Fake_Statement), (b:Fake_Statement)
            WHERE ID(a) = $start_id AND ID(b) = $end_id
            CALL apoc.algo.dijkstra(a, b, 'HAS_KEYWORD', "weight", 1, 2) YIELD path, weight
            RETURN path, weight
        '''
        with self.driver.session() as session:
            records, summary, keys = self.driver.execute_query(FIND_PATH, start_id=start_id, end_id=end_id)
            paths = [p.data() for p in records]
            return paths

    def find_similar(self, id):
        querry = '''
        MATCH (p1:Fake_Statement)-[r:SIMILAR]->(p2:Fake_Statement)
        WHERE p1.id=$id
        RETURN distinct(p2), p1.statement AS origin, p2.statement AS statement, r.score AS similarity, p2.community as community
        ORDER BY similarity DESCENDING
        '''
        with self.driver.session() as session:
            records, summary, keys = self.driver.execute_query(
                querry,
                database_="news", id=id
            )
            elements = [p.data() for p in records]
            return elements

    def find_similar_baseline(self, id):
        querry = '''
                MATCH (p1:Fake_Statement)-[:HAS_KEYWORD]->(k)-[:HAS_KEYWORD]-(p2:Fake_Statement)
                WHERE p1.id=$id
                WITH distinct(p2)
                RETURN COLLECT(p2.community) as communities
                '''
        with self.driver.session() as session:
            records, summary, keys = self.driver.execute_query(
                querry,
                database_="news", id=id
            )
            elements = [p.data() for p in records]
            return elements

    def knn(self):
        gds = GraphDataScience(NEO4J_URI, auth=NEO4J_AUTH)
        gds.set_database("news")

        node_projection = ["Person", "Fake_Statement", "Entity"]
        relationship_projection = {"HAS_KEYWORD": {"orientation": "UNDIRECTED"}}
        result = gds.graph.project.estimate(node_projection, relationship_projection)
        # print(f"Required memory for native loading: {result['requiredMemory']}")
        try:
            G = gds.graph.get("purchases")
            gds.graph.drop(G, False)
        except:
            print("No previous projection found")
            pass
        G, result = gds.graph.project("purchases", node_projection, relationship_projection)
        # print(f"The projection took {result['projectMillis']} ms")

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
        # print(f"Number of embedding vectors produced: {result['nodePropertiesWritten']}")

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

        # print(f"Relationships produced: {result['relationshipsWritten']}")
        # print(f"Nodes compared: {result['nodesCompared']}")
        # print(f"Mean similarity: {result['similarityDistribution']['mean']}")
