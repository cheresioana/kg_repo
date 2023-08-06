import json
import time
from urllib.parse import urlparse

import requests
from neo4j import GraphDatabase, basic_auth


class NeoConnector:
    def __init__(self):
        self.driver = GraphDatabase.driver('bolt://localhost:7687', auth=basic_auth('neo4j', 'ioana123'))
        self.dic_key = {
            'CARDINAL': 'MENTIONS_CARDINAL',
            'DATE': 'MENTIONS_DATE',
            'EVENT': 'MENTIONS_EVENT',
            'FAC': 'MENTIONS_BUILDING',
            'GPE': 'MENTIONS_GEO_ENTITIES',
            'LANGUAGE': 'MENTIONS_LANGUAGE',
            'LAW': 'MENTIONS_DOCUMENTS',
            'LOC': 'MENTIONS_LOCATION',
            'MONEY': 'MENTIONS_MONEY',
            'NORP': 'MENTIONS_AFFILIATION',
            'ORDINAL': 'MENTIONS_ORDINAL',
            'ORG': 'MENTIONS_ORGANIZATION',
            'PERCENT': 'MENTIONS_PERCENT',
            'PERSON': 'MENTIONS_PERSON',
            'PRODUCT': 'MENTIONS_PRODUCT',
            'QUANTITY': 'MENTIONS_QUANTITY',
            'TIME': 'MENTIONS_TIME',
            'WORK_OF_ART': 'MENTIONS_ART',
            'simple_keyword': 'HAS_KEYWORD'}
        self.wikidata_query = "https://query.wikidata.org/bigdata/namespace/wdq/sparql?query="

    def close(self):
        self.driver.close()

    def insert_statement(self, row):
        INSERT_STATEMENT = """USE news
            UNWIND $inputs AS row
            MERGE (n:Fake_Statement {id: row.id}) 
            SET n.statement = row.statement    
        """
        with self.driver.session() as session:
            session.run(INSERT_STATEMENT, inputs=row.to_dict())

    def insert_statement_entities(self, row, entities):
        entity_keys = list(entities.keys())
        for key in entity_keys:
            if key == 'PERSON':
                self.__insert_person_entities(row, entities[key])
            else:
                self.insert_simple_entity(row, entities, key)

    def insert_simple_entity(self, row, entities, key):
        QUERY_ENTITIES = """USE news
            UNWIND $inputs AS doc
            UNWIND $ent AS ents

            MATCH (n:Fake_Statement {id: doc.id})
             FOREACH(entity IN $ent |
                MERGE (e:Entity {name: entity})
                MERGE (n)-[:""" + self.dic_key[key] + """]->(e)
                MERGE (n)-[:HAS_KEYWORD]->(e)
            )"""

        with self.driver.session() as session:
            session.run(QUERY_ENTITIES, ent=entities[key], key=key, inputs=row.to_dict())

    def __get_label_query(self, entity):
        return 'SELECT ?entity ?entityLabel ?id WHERE\n{?entity rdfs:label "' + str(
            entity) + '"@en.\n?entity wdt:P31 wd:Q5. \n SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }\n}'

    def __insert_person(self, row, official_name, uri='', status='unkown'):
        QUERY_PERSON = """USE news
            UNWIND $inputs AS doc
            MATCH (n:Fake_Statement {id: doc.id})
                MERGE (e:Person {name: $name, status: $status, uri: $uri})
                MERGE (n)-[:MENTIONS_PERSON]->(e)
                MERGE (n)-[:HAS_KEYWORD]->(e)
                """
        with self.driver.session() as session:
            session.run(QUERY_PERSON, inputs=row.to_dict(), name=official_name,
                        status=status, uri=uri)

    def __make_query(self, query, row):
        try_index = 0
        response = requests.get(query, params={'format': "json"})
        while response.status_code != 200 and try_index < 5:
            response = requests.get(query, params={'format': "json"})
            try_index = try_index + 1
            time.sleep(2)
        if try_index >= 5:
            print("error for request")
            print(response)
            print(response.text)
            print(row)
            return None
        return response.json()['results']['bindings']

    def __insert_search_person(self, row, entity):
        SPARQL_QUERY_LIST_MATCHINGS = """
            SELECT * WHERE {
              SERVICE wikibase:mwapi {
                  bd:serviceParam wikibase:endpoint "www.wikidata.org";
                                  wikibase:api "EntitySearch";
                                  mwapi:search """ + '"' + entity + '"' """;
                                  mwapi:language "en".
                  ?item wikibase:apiOutputItem mwapi:item.
                  ?num wikibase:apiOrdinal true.
              }
              ?item wdt:P31 wd:Q5
            } ORDER BY ASC(?num) LIMIT 20
            """
        jsonResponse = self.__make_query(self.wikidata_query + SPARQL_QUERY_LIST_MATCHINGS, row)
        if jsonResponse and len(jsonResponse) > 0:
            entity_url = jsonResponse[0]['item']['value']
            path = urlparse(entity_url).path
            entity_id = path.split('/')[-1]
            SPARQL_QUERY6 = f"""
                            SELECT ?label WHERE {{
                              wd:{entity_id} rdfs:label ?label .
                              FILTER(LANG(?label) = "en") .
                            }}
                            """
            jsonResponse = self.__make_query(self.wikidata_query + SPARQL_QUERY6, row)
            # response = requests.get(, params={'format': "json"})
            try:
                official_name = jsonResponse[0]['label']['value']
                uri = jsonResponse[0]['label']['value']
                self.__insert_person(row, official_name, uri, status="known")
                return 1
            except:
                return -1
        return -1

    def __insert_person_entities(self, row, entities):
        for entity in entities:
            my_entity = entity
            if "elensk" in entity:
                my_entity = "Volodymyr Zelenskyy"
            qstr = self.__get_label_query(my_entity)
            response = requests.get(self.wikidata_query + qstr, params={'format': "json"})
            if response.status_code == 200:
                try:
                    # here I try exact matching
                    official_name = response.json()['results']['bindings'][0]['entityLabel']['value']
                    uri = response.json()['results']['bindings'][0]['entity']['value']
                    self.__insert_person(row, official_name, uri, status="known")
                except:
                    # in case there is no exact matching I use wikidata search engine
                    print(f'Searching for entity:{entity}')
                    self.__insert_search_person(row, entity)
            else:
                print(f'The request failed for entity:{entity}')

    def set_similarity(self):
        SET_SIMILARITY_QUERY = '''
        USE news
        MATCH (n:Fake_Statement)-[:HAS_KEYWORD]->(k)<-[:HAS_KEYWORD]-(n2:Fake_Statement)
        WHERE n <> n2
        WITH n, n2, collect(id(k)) AS kws_shared
        WHERE size(kws_shared) > 2
        MATCH (n)-[:HAS_KEYWORD]->(k)
        WITH n, n2, kws_shared, collect(id(k)) AS kws1
        MATCH (n2)-[:HAS_KEYWORD]->(k)
        WITH n, n2, kws_shared, kws1, collect(id(k)) AS kws2
        WITH n, n2, 1.0 * size(kws_shared) / (size(kws1) + size(kws2)  - size(kws_shared)) AS similarity
        MERGE (n)-[r:SIMILAR_TO]-(n2)
        SET r.similarity = similarity
        '''
        with self.driver.session() as session:
            response = session.run(SET_SIMILARITY_QUERY)
            print(response)

    @staticmethod
    def _create_and_return_greeting(tx):
        result = tx.run("USE news "
                        "MATCH(p:Fake_Statement)"
                        "RETURN p")
        return result.single()[0]

    def select_fake_statements(self):
        with self.driver.session() as session:
            records, summary, keys = self.driver.execute_query(
                "USE news MATCH(p:Fake_Statement) return p",
                database_="news"
            )

            # Loop through results and do something with them
            for person in records:
                print(person)

    def select_communities(self):
        with self.driver.session() as session:
            records = session.run(
                "USE news MATCH(p:Fake_Statement) return p.community as community",
                database_="news"
            )
            results = [record for record in records.data()]
            communities = list(set([result["community"] for result in results]))
            print(communities)
            print(len(communities))

            for community_id in communities:
                records, summary, keys = self.driver.execute_query(
                    "USE news "
                    "MATCH (p:Fake_Statement)"
                    " WHERE p.community=$community"
                    " return p.statement as statement, p.id as id",
                    database_="news",
                    community=community_id
                )
                print(records)
                results = [record for record in records]
                print(results)
                exit(0)

            # Loop through results and do something with them
            # print(results)
            # for person in results:
            #    print(person)
            #    print(person["id"])

    def get_louvain_simple(self):
        CREATE_PROJECTION_QUERY = '''
        USE news
        CALL gds.graph.project(
        'myGraph',
        'Fake_Statement',
        {
            SIMILAR_TO: {
                orientation: 'UNDIRECTED'
            }
        }
        )
        CALL gds.louvain.stream('myGraph')
        YIELD nodeId, communityId, intermediateCommunityIds
        RETURN gds.util.asNode(nodeId).statement AS name, communityId
        ORDER BY name ASC 
        '''
        GET_DATA_QUERY = '''
        USE news
        match (p:Fake_Statement)-[r:HAS_KEYWORD]-(k) 
        WHERE p.community=114 
        WITH p, k, count(r) as rel_cnt, r
        return p, k, r, rel_cnt
        '''
        with self.driver.session() as session:
            response = session.run(GET_DATA_QUERY)
            print(response)


    def _get_statement_nodes(self):
        with self.driver.session() as session:
            records, summary, keys = self.driver.execute_query(
                "USE news "
                "MATCH(p:Fake_Statement)-[:HAS_KEYWORD]-(n) "
                "return DISTINCT p, p.id as intra_id, p.statement as statement, "
                "'fake_news' as tag, ID(p) as id, "
                "p.community as community",
                database_="news"
            )
            statements = [p.data() for p in records]
            return statements
    def _get_top_keywords(self, limit=50):
        with self.driver.session() as session:
            records, summary, keys = self.driver.execute_query(
                '''
            MATCH (n)--()
            WHERE not n:Fake_Statement
            WITH n, apoc.node.degree(n) as degree
            return DISTINCT(n) , n.name as name, degree, labels(n)[0] as tag, ID(n) as id
            ORDER BY degree DESC
            LIMIT $limit
            ''', database_="news", limit=limit)
            key_elements = [p.data() for p in records]
            return key_elements

    def _get_links(self, id_list1, id_list2):
        with self.driver.session() as session:
            records, summary, keys = self.driver.execute_query(
                '''
            MATCH (n)-[:HAS_KEYWORD]-(p)
            WHERE ID(n) in $id_list1 and ID(p) in $id_list2
            RETURN ID(n) AS source, ID(p) AS target
            ''', database_="news", id_list1=id_list1, id_list2=id_list2)
            links = [p.data() for p in records]
            return links

    def _get_statement_nodes_from_list(self, list):
        with self.driver.session() as session:
            records, summary, keys = self.driver.execute_query(
                "USE news "
                "MATCH(p:Fake_Statement)"
                "WHERE ID(p) in $id_list "
                "return p.id as intra_id, p.statement as statement, "
                "'fake_news' as tag, ID(p) as id, "
                "p.community as community",
                database_="news", id_list=list
            )
            statements = [p.data() for p in records]
            return statements

    def get_kg(self):

            statements = self._get_statement_nodes()
            key_elements = self._get_top_keywords()
            id_statements = [statement["id"] for statement in statements]
            id_keys = [key["id"] for key in key_elements]

            links = self._get_links(id_statements, id_keys)
            id_statements_linked = list(set([link['source'] for link in links]))
            statements = self._get_statement_nodes_from_list(id_statements_linked)
            print(len(statements))
            print(len(id_keys))
            #print(len(links))
            #print(len(list(set(links))))
            statements.extend(key_elements)
            data = {
                'nodes' : statements,
                'links': links
            }

            return data

    def get_similar(self, id):
        with self.driver.session() as session:
            records, summary, keys = self.driver.execute_query(
                "USE news "
                "MATCH (p:Fake_Statement)-[r:SIMILAR_TO]-(k)" 
                "WHERE ID(p)=$id and p.community=k.community "
                "return k.id as intra_id, k.statement as statement, "
                "'fake_news' as tag, ID(k) as id",
                database_="news", id=int(id),
            )
            statements = [p.data() for p in records]
            records, summary, keys = self.driver.execute_query(
                "USE news "
                "MATCH (p:Fake_Statement)-[r:SIMILAR_TO]-(k)"
                "WHERE ID(p)=$id and p.community=k.community "
               "RETURN ID(p) AS source, ID(k) AS target",
                database_="news", id=int(id),
            )
            links = [p.data() for p in records]
            my_dict = {
                'nodes': statements,
                'links': links,
            }
            return my_dict



'''
MATCH (n:Fake_Statement)-[g]->(k)<-[r]-(n2:Fake_Statement)
WHERE n <> n2
WITH n, n2, collect(id(k)) AS kws_shared
WHERE size(kws_shared) > 2
MATCH (n)-[g]->(k)
WITH n, n2, kws_shared, collect(id(k)) AS kws1
MATCH (n2)-[r]->(k)
WITH n, n2, kws_shared, kws1, collect(id(k)) AS kws2
WITH n, n2, 1.0 * size(kws_shared) / (size(kws1) + size(kws2)  - size(kws_shared)) AS similarity
MERGE (n)-[r:SIMILAR_TO]-(n2)
SET r.similarity = similarity
'''

'''

MATCH (n)-[r:SIMILAR_TO]-(n2)
return n, r, n2

'''
