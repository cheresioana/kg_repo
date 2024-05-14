import json
import time
from urllib.parse import urlparse

import requests
from neo4j import GraphDatabase, basic_auth

from DataObject.SubGraphResult import Node, BigNode, FakeStatement, SimpleNode
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from constanst import NEO4J_URI, NEO4J_AUTH


class NeoConnector:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH)
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
        self.dic_key_accepted = {
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
            'PERSON': 'MENTIONS_PERSON',
            'PRODUCT': 'MENTIONS_PRODUCT',
            'simple_keyword': 'HAS_KEYWORD'}
        self.wikidata_query = "https://query.wikidata.org/bigdata/namespace/wdq/sparql?query="

    def close(self):
        self.driver.close()

    def insert_statement(self, row, tokens=[]):
        INSERT_STATEMENT = """USE neo4j
            UNWIND $inputs AS row
            MERGE (n:Fake_Statement {url:row.debunking_link}) 
            SET n.statement = row.statement, n.id = ID(n), n.intra_id = ID(n), n.words=$tokens, n.date=row.date, 
            n.formatted_date=apoc.date.format(apoc.date.parse(row.date, 'ms', 'dd.MM.yyyy'),'ms', 'yyyy.MM.dd'),
            n.embedding = row.embedding
            RETURN n
        """
        with self.driver.session() as session:
            records, summary, keys = self.driver.execute_query(INSERT_STATEMENT, inputs=row.to_dict(), tokens=tokens)
            if len(records) > 0:
                record = records[0].data()['n']
                return record['id']

    def insert_search_statement(self, statement, query_embedding, keywords):
        INSERT_STATEMENT = """USE neo4j
            MERGE (n:Fake_Statement {statement: $input, embedding: $embedding, words: $keywords}) 
            SET n.query = 1, n.id = ID(n), n.tag='query', n.intra_id = ID(n)
            RETURN n   
        """
        with self.driver.session() as session:
            records, summary, keys = self.driver.execute_query(INSERT_STATEMENT, input=statement,
                                                               embedding=query_embedding, keywords=keywords)
            if len(records) > 0:
                record = records[0].data()['n']
                return Node(record['intra_id'], record['statement'], record['id'], record['tag'])
                # return records[0]['id']

        return None

    def insert_statement_entities(self, doc_id, entities):
        entity_keys = list(entities.keys())
        for key in entity_keys:
                # if key == 'PERSON':
                #     self.__insert_person_entities(doc_id, entities[key])
                # else:
                self.insert_simple_entity(doc_id, entities, key)

    def insert_simple_entity(self, doc_id, entities, key):
        QUERY_ENTITIES = """USE neo4j
            UNWIND $ent AS ents

            MATCH (n:Fake_Statement {id: $doc_id})
             FOREACH(entity IN $ent |
                MERGE (e:Entity {name: entity, type:$key})
                SET e.intra_id = ID(e)
                MERGE (n)-[:HAS_KEYWORD {weight:1}]->(e)
            )"""
        # Missing  MERGE (n)-[:""" + self.dic_key[key] + """]->(e)
        with self.driver.session() as session:
            session.run(QUERY_ENTITIES, ent=entities[key], key=key, doc_id=doc_id)

    def insert_location(self, doc_id, location):
        QUERY_ENTITIES = """USE neo4j
            MATCH (n:Fake_Statement {id: $doc_id})
            MERGE (e:Location {location: $location, name: $location})
            MERGE (n)-[:HAS_LOCATION]->(e)
            """
        with self.driver.session() as session:
            session.run(QUERY_ENTITIES, location=location, doc_id=doc_id)

    def insert_words(self, id, words):
        QUERY_ENTITIES = """USE neo4j
            MATCH (n:Fake_Statement {id: $id})
            SET n.words = $words
            """
        with self.driver.session() as session:
            session.run(QUERY_ENTITIES, words=words, id=id)

    def insert_language(self, doc_id, lang):
        QUERY_ENTITIES = """USE neo4j
               MATCH (n:Fake_Statement {id: $doc_id})
               MERGE (e:Language {name: $lang})
               MERGE (n)-[:HAS_LANGUAGE]->(e)
               """
        with self.driver.session() as session:
            session.run(QUERY_ENTITIES, lang=lang, doc_id=doc_id)

    def insert_channel(self, doc_id, channel):
        QUERY_ENTITIES = """USE neo4j
            MATCH (n:Fake_Statement {id: $doc_id})
            MERGE (e:Channel {name: $channel})
            MERGE (n)-[:HAS_CHANNEL]->(e)
            """
        with self.driver.session() as session:
            session.run(QUERY_ENTITIES, channel=channel, doc_id=doc_id)

    def __get_label_query(self, entity):
        return 'SELECT ?entity ?entityLabel ?id WHERE\n{?entity rdfs:label "' + str(
            entity) + '"@en.\n?entity wdt:P31 wd:Q5. \n SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }\n}'

    def __insert_person(self, doc_id, official_name, uri='', status='unknown'):
        QUERY_PERSON = """USE neo4j
            
            MATCH (n:Fake_Statement {id: $doc_id})
                MERGE (e:Person {name: $name, status: $status, uri: $uri})
                SET e.intra_id = ID(e)
                MERGE (n)-[:MENTIONS_PERSON {weight:1}]->(e)
                """

        # Missing MERGE (n)-[:MENTIONS_PERSON]->(e)
        with self.driver.session() as session:
            session.run(QUERY_PERSON, doc_id=doc_id, name=official_name,
                        status=status, uri=uri)

    def __make_query(self, query):
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
            return None
        return response.json()['results']['bindings']

    def __insert_search_person(self, doc_id, entity):
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
        jsonResponse = self.__make_query(self.wikidata_query + SPARQL_QUERY_LIST_MATCHINGS)
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
            jsonResponse = self.__make_query(self.wikidata_query + SPARQL_QUERY6)
            # response = requests.get(, params={'format': "json"})
            try:
                official_name = jsonResponse[0]['label']['value']
                uri = jsonResponse[0]['label']['value']
                self.__insert_person(doc_id, official_name, uri, status="known")
                return 1
            except:
                return -1
        else:
            self.__insert_person(doc_id, entity)

    def __insert_person_entities(self, doc_id, entities):
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
                    print(f"From {entity} to {official_name}")
                    self.__insert_person(doc_id, official_name, uri, status="known")
                except:
                    # in case there is no exact matching I use wikidata search engine
                    print(f'Searching for entity:{entity}')
                    self.__insert_search_person(doc_id, entity)
            else:
                print(f'The request failed for entity:{entity}')

    def set_similarity(self):
        SET_SIMILARITY_QUERY = '''
        USE neo4j
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
        result = tx.run("USE neo4j "
                        "MATCH(p:Fake_Statement)"
                        "RETURN p")
        return result.single()[0]

    def select_fake_statements(self):
        with self.driver.session() as session:
            records, summary, keys = self.driver.execute_query(
                "USE neo4j MATCH(p:Fake_Statement) return p",
                database_="neo4j"
            )
            # Loop through results and do something with them
            for person in records:
                print(person)

    def select_communities(self):
        with self.driver.session() as session:
            records = session.run(
                "USE neo4j MATCH(p:Fake_Statement) return p.community as community",
                database_="neo4j"
            )
            results = [record for record in records.data()]
            communities = list(set([result["community"] for result in results]))
            print(communities)
            print(len(communities))

            for community_id in communities:
                records, summary, keys = self.driver.execute_query(
                    "USE neo4j "
                    "MATCH (p:Fake_Statement)"
                    " WHERE p.community=$community"
                    " return p.statement as statement, p.id as id",
                    database_="neo4j",
                    community=community_id
                )
                print(records)
                results = [record for record in records]
                print(results)
                exit(0)

    def get_louvain_simple(self):
        CREATE_PROJECTION_QUERY = '''
        USE neo4j
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
        USE neo4j
        match (p:Fake_Statement)-[r:HAS_KEYWORD]-(k) 
        WHERE p.community=114 
        WITH p, k, count(r) as rel_cnt, r
        return p, k, r, rel_cnt
        '''
        with self.driver.session() as session:
            session.run(CREATE_PROJECTION_QUERY)

    def run_louvain_algorithm(self):
        DROP_IF_EXISTS = '''
        USE neo4j
        CALL gds.graph.drop('myGraph', false) YIELD graphName;
        '''
        with self.driver.session() as session:
            records, summary, keys = self.driver.execute_query(DROP_IF_EXISTS)
            print(records)
            print(summary)

        CREATE_PROJECTION_QUERY = '''
        USE neo4j
       CALL gds.graph.project(
        'myGraph',
        'Fake_Statement',
        {
            SIMILAR_TO: {
                orientation: 'UNDIRECTED'
            }
        }
        )'''
        with self.driver.session() as session:
            records, summary, keys = self.driver.execute_query(CREATE_PROJECTION_QUERY)
            print(records)
            print(summary)

        WRITE_COMMUNITY = '''
        USE neo4j
        CALL gds.louvain.write('myGraph', { writeProperty: 'community' })
        YIELD communityCount, modularity, modularities
        '''
        with self.driver.session() as session:
            records, summary, keys = self.driver.execute_query(WRITE_COMMUNITY)
            print(records)
            print(summary)

    def _get_connected_statements(self, keywords_ids):
        print(keywords_ids)
        with self.driver.session() as session:
            statements = []
            for key_id in keywords_ids:
                records, summary, keys = self.driver.execute_query(
                    "USE neo4j "
                    "MATCH(p:Fake_Statement)--(n) "
                    "WHERE ID(n) = $keyword_id "
                    "WITH apoc.node.degree(p) as degree, p "
                    "return DISTINCT p, p.id as intra_id, p.statement as statement, "
                    "'fake_news' as tag, ID(p) as id, "
                    " p.community as community, degree"
                    " ORDER BY degree DESC "
                    "LIMIT $limit",

                    database_="neo4j", limit=25, keyword_id=key_id
                )
                statements.extend([p.data() for p in records])
            return statements

    def _get_statement_nodes(self, limit=200):
        with self.driver.session() as session:
            records, summary, keys = self.driver.execute_query(
                "USE neo4j "
                "MATCH(p:Fake_Statement)-[:HAS_KEYWORD]-(n) "
                "WITH apoc.node.degree(p) as degree, p "
                "return DISTINCT p, p.id as intra_id, p.statement as statement, "
                "'fake_news' as tag, ID(p) as id, "
                " p.community as community, degree"
                "   ORDER BY degree DESC"
                " LIMIT $limit",
                database_="neo4j", limit=limit
            )
            statements = [p.data() for p in records]
            return statements

    def _get_top_keywords(self, limit=12):
        with self.driver.session() as session:
            records, summary, keys = self.driver.execute_query(
                '''
            MATCH (n)--(c:Fake_Statement)
            WHERE not n:Fake_Statement
            WITH n, count(*) as degree
            return DISTINCT(n) , n.name as name, degree, labels(n)[0] as tag, ID(n) as id
            ORDER BY degree DESC
            LIMIT $limit
            ''', database_="neo4j", limit=limit)
            key_elements = [p.data() for p in records]
            return key_elements

    def _get_links(self, id_list1, id_list2):
        with self.driver.session() as session:
            records, summary, keys = self.driver.execute_query(
                '''
            MATCH (n)--(p)
            WHERE ID(n) in $id_list1 and ID(p) in $id_list2
            RETURN ID(n) AS source, ID(p) AS target
            ''', database_="neo4j", id_list1=id_list1, id_list2=id_list2)
            links = [p.data() for p in records]
            return links

    def _get_statement_nodes_from_list(self, list):
        with self.driver.session() as session:
            records, summary, keys = self.driver.execute_query(
                "USE neo4j "
                "MATCH(p:Fake_Statement)"
                "WHERE ID(p) in $id_list "
                "return p.id as intra_id, p.statement as statement, "
                "'fake_news' as tag, ID(p) as id, "
                "p.community as community",
                database_="neo4j", id_list=list
            )
            statements = [p.data() for p in records]
            return statements

    def get_kg(self):

        #statements = self._get_statement_nodes()
        key_elements = self._get_top_keywords()
        id_keys = [key["id"] for key in key_elements]
        statements = self._get_connected_statements(keywords_ids=id_keys)

        id_statements = [statement["id"] for statement in statements]


        links = self._get_links(id_statements, id_keys)
        id_statements_linked = list(set([link['source'] for link in links]))
        statements = self._get_statement_nodes_from_list(id_statements_linked)
        print(len(statements))
        print(len(id_keys))
        # print(len(links))
        # print(len(list(set(links))))
        statements.extend(key_elements)
        data = {
            'nodes': statements,
            'links': links
        }

        return data

    def get_community_subgraph(self, id):
        with self.driver.session() as session:
            records, summary, keys = self.driver.execute_query(
                "USE neo4j "
                "MATCH (n) WHERE n.id=$id return n",
                database_="neo4j", id=int(id),
            )
            origins = [p.data()['n'] for p in records]
            records, summary, keys = self.driver.execute_query(
                "USE neo4j "
                "MATCH (n)-[:SIMILAR_TO]-(p) WHERE p.community=n.community AND n.id=$id return p",
                database_="neo4j", id=int(id),
            )
            statements = [p.data()['p'] for p in records]

            records, summary, keys = self.driver.execute_query(
                "USE neo4j "
                "MATCH (n)-[:SIMILAR_TO]-(p), (n)-[:HAS_KEYWORD]-(d)-[:HAS_KEYWORD]-(p) "
                "WHERE p.community=n.community AND "
                "n.id=$id return DISTINCT(ID(d)) as id, d.name as statement, 'key_element' as tag",
                database_="neo4j", id=int(id),
            )
            key_elements = [p.data() for p in records]

            records, summary, keys = self.driver.execute_query(
                "USE neo4j "
                "MATCH (n)-[r:SIMILAR_TO]-(p), (n)-[:HAS_KEYWORD]-(d)-[:HAS_KEYWORD]-(p) WHERE p.community=n.community AND n.id=$id return n.id as "
                "source, ID(d) as target, 'fake_news' as tag",
                database_="neo4j", id=int(id),
            )
            links = [p.data() for p in records]

            records, summary, keys = self.driver.execute_query(
                "USE neo4j "
                "MATCH (n)-[r:SIMILAR_TO]-(p), (n)-[:HAS_KEYWORD]-(d)-[:HAS_KEYWORD]-(p) WHERE p.community=n.community AND n.id=$id return "
                "ID(d) as source, p.id as target",
                database_="neo4j", id=int(id),
            )
            links2 = [p.data() for p in records]

            statements.extend(origins)
            statements.extend(key_elements)
            links.extend(links2)

            print('ORIGIN')
            print(origins)

            print('STATEMENTS')
            print(statements)

            print('LINKS')
            print(links)

            data = {
                'origin': origins,
                'nodes': statements,
                'links': links
            }

            return data

    def get_community_detected_subgraph(self, id, community_id):
        with self.driver.session() as session:
            # here I take the statement
            records, summary, keys = self.driver.execute_query(
                "USE neo4j "
                "MATCH (n) WHERE n.id=$id return n",
                database_="neo4j", id=int(id),
            )
            origins = []
            for p in records:
                g = p.data()['n']
                g['tag'] = 'fake_news'
                g['intra_id'] = g['id']
                origins.append(g)
            # origins = [p.data()['n'] for p in records]

            # here I find the most similar statements
            querry = '''
                   MATCH (p1:Fake_Statement)-[r:SIMILAR]->(p2:Fake_Statement)
                   WHERE p1.id=$id and p2.community=$comm
                   RETURN distinct(p2), r.score as similarity
                   ORDER BY similarity DESCENDING LIMIT 3
                   '''
            records, summary, keys = self.driver.execute_query(
                querry,
                database_="neo4j", id=id, comm=community_id
            )
            statements = []
            for p in records:
                g = p.data()['p2']
                g['tag'] = 'fake_news'
                g['intra_id'] = g['id']
                statements.append(g)
            # statements = [p.data()["p2"] for p in records]

            ids = [p["id"] for p in statements]
            records, summary, keys = self.driver.execute_query(
                "USE neo4j "
                "MATCH (n)-[:HAS_KEYWORD]-(d)-[:HAS_KEYWORD]-(p) "
                "WHERE p.id in $ids AND n.id=$id "
                " return DISTINCT(ID(d)) as id, d.name as statement, 'key_element' as tag",
                database_="neo4j", id=int(id), ids=ids
            )
            key_elements = [p.data() for p in records]
            ids_key = [p["id"] for p in key_elements]

            records, summary, keys = self.driver.execute_query(
                "USE neo4j "
                "MATCH (n)-[:HAS_KEYWORD]-(d)"
                "WHERE n.id=$id  and ID(d) in $ids return n.id as "
                "source, ID(d) as target, 'fake_news' as tag",
                database_="neo4j", id=int(id), ids=ids_key
            )
            links = [p.data() for p in records]
            for p in links:
                p["value"] = 4

            records, summary, keys = self.driver.execute_query(
                "USE neo4j "
                "MATCH (n)-[:HAS_KEYWORD]-(d)"
                "WHERE ID(d) in $ids_key  and n.id in $ids return n.id as "
                "target, ID(d) as source, 'fake_news' as tag",
                database_="neo4j", id=int(id), ids_key=ids_key, ids=ids
            )
            links2 = [p.data() for p in records]
            for p in links2:
                p["value"] = 2

            statements.extend(origins)
            statements.extend(key_elements)
            links.extend(links2)
            # links = []
            print('ORIGIN')
            print(origins)

            print('STATEMENTS')
            print(statements)

            print('LINKS')
            print(links)

            data = {
                'origin': origins,
                'nodes': statements,
                'links': links
            }

            return data

    def get_community_not_detected_subgraph(self, id):
        with self.driver.session() as session:
            records, summary, keys = self.driver.execute_query(
                "USE neo4j "
                "MATCH (n) WHERE n.id=$id return n",
                database_="neo4j", id=int(id),
            )
            origins = [p.data()['n'] for p in records]
            records, summary, keys = self.driver.execute_query(
                "USE neo4j "
                "MATCH (n)-[:HAS_KEYWORD]-(p)-[:HAS_KEYWORD]-(d) WHERE n.id=$id return d LIMIT 5",
                database_="neo4j", id=int(id),
            )
            statements = [p.data()['d'] for p in records]
            ids = [p["id"] for p in statements]

            records, summary, keys = self.driver.execute_query(
                "USE neo4j "
                "MATCH (n)-[:HAS_KEYWORD]-(p)-[:HAS_KEYWORD]-(d) WHERE n.id=$id and d.id in $ids "
                "return DISTINCT(ID(p)) as id, p.name as statement, 'key_element' as tag",
                database_="neo4j", id=int(id), ids=ids
            )
            keywords = [p.data() for p in records]
            print("keywords")
            print(keywords)

            records, summary, keys = self.driver.execute_query(
                "USE neo4j "
                "MATCH (n)-[:HAS_KEYWORD]-(p)-[:HAS_KEYWORD]-(d) "
                "WHERE n.id=$id AND d.id in $ids"
                " return n.id as "
                "source, ID(p) as target, 'fake_news' as tag",
                database_="neo4j", id=int(id), ids=ids
            )
            links = [p.data() for p in records]

            records, summary, keys = self.driver.execute_query(
                "USE neo4j "
                "MATCH (n)-[:HAS_KEYWORD]-(p)-[:HAS_KEYWORD]-(d) "
                "WHERE n.id=$id AND d.id in $ids"
                " return d.id as "
                "source, ID(p) as target, 'fake_news' as tag",
                database_="neo4j", id=int(id), ids=ids
            )
            links2 = [p.data() for p in records]

            statements.extend(origins)
            statements.extend(keywords)
            links.extend(links2)

            print('ORIGIN')
            print(origins)

            print('STATEMENTS')
            print(statements)

            print('LINKS')
            print(links)

            data = {
                'origin': origins,
                'nodes': statements,
                'links': links
            }

            return data

    def get_subgraph(self, ids):
        nodes = []
        nodes_ids = []
        links = []
        for id in ids:
            with self.driver.session() as session:
                records, summary, keys = self.driver.execute_query(
                    "USE neo4j "
                    "MATCH (p:Fake_Statement)--(k) "
                    "WHERE p.intra_id=$id "
                    "return p, collect({node: k, type: labels(k)}) as n",
                    database_="neo4j", id=int(id),
                )
                statements = [p.data() for p in records]
                fs = statements[0]['p']
                fs_id = fs['intra_id']
                fs_node = BigNode('Fake_Statement', fs_id, 0,
                            FakeStatement(fs['formatted_date'],
                                          fs['intra_id'], fs['statement'],
                                          fs['words'],
                                          fs['url']))
                nodes.append(fs_node)
                nodes_ids.append(fs['intra_id'])
                for e in statements[0]['n']:
                    e_id = e['node']['intra_id']
                    if e_id not in nodes_ids:
                        nodes.append(
                            BigNode(e['type'][0],e_id,1,
                                    SimpleNode(e['node']['name'],e['type'][0],
                                                  e_id))
                        )
                        fs_node.increase_connections()
                        nodes_ids.append(e_id)
                    else:
                        for element in nodes:
                            if element.id == e_id:
                                element.increase_connections()
                                break;
                    links.append({'source': fs_id, 'target': e_id})
        return nodes, links



    def get_similar(self, id):
        with self.driver.session() as session:
            records, summary, keys = self.driver.execute_query(
                "USE neo4j "
                "MATCH (p:Fake_Statement)-[r:SIMILAR_TO]-(k)"
                "WHERE ID(p)=$id and p.community=k.community "
                "return k.id as intra_id, k.statement as statement, "
                "'fake_news' as tag, ID(k) as id",
                database_="neo4j", id=int(id),
            )
            statements = [p.data() for p in records]
            records, summary, keys = self.driver.execute_query(
                "USE neo4j "
                "MATCH (p:Fake_Statement)-[r:SIMILAR_TO]-(k)"
                "WHERE ID(p)=$id and p.community=k.community "
                "RETURN ID(p) AS source, ID(k) AS target",
                database_="neo4j", id=int(id),
            )
            links = [p.data() for p in records]
            my_dict = {
                'nodes': statements,
                'links': links,
            }
            return my_dict

    def get_communities(self):
        querry = '''
            MATCH (p)
            WITH DISTINCT(p.community) as comm_id, COUNT(p) as Total_number
            MATCH (q:Fake_Statement)
            WHERE q.community = comm_id
            WITH comm_id, Total_number, COUNT(q) as Fake_S
            // For each community, find the Fake_Statement with the most relationships
            OPTIONAL MATCH (most_connected:Fake_Statement)-[r]-()
            WHERE most_connected.community = comm_id
            WITH comm_id, Total_number, Fake_S, COLLECT(most_connected) as statements
            RETURN comm_id, Total_number, Fake_S, statements;
        '''
        with self.driver.session() as session:
            records, summary, keys = self.driver.execute_query(
                querry,
                database_="neo4j",
            )
            statements = [p.data() for p in records]
        return statements

    def get_popular_statements_communities(self):
        querry = '''
            MATCH (p)
            WITH DISTINCT(p.community) as comm_id, COUNT(p) as Total_number
            MATCH (q:Fake_Statement)
            WHERE q.community = comm_id
            WITH comm_id, Total_number, COUNT(q) as Fake_S
            // For each community, find the Fake_Statement with the most relationships
            OPTIONAL MATCH (most_connected:Fake_Statement)-[r]-()
            WHERE most_connected.community = comm_id
            WITH comm_id, Total_number, Fake_S, most_connected, COUNT(r) as rel_count
            ORDER BY rel_count DESC
            WITH comm_id, Total_number, Fake_S, COLLECT(most_connected.id) as statements
            RETURN comm_id, Total_number, Fake_S, statements;
        '''
        with self.driver.session() as session:
            records, summary, keys = self.driver.execute_query(
                querry,
                database_="neo4j",
            )
            statements = [p.data() for p in records]
        return statements

    def get_statements_vectors(self):
        query = '''
            USE neo4j
            MATCH (p:Fake_Statement)
            WHERE p.embedding IS NOT NULL 
            RETURN p.id as id, ID(p) as intra_id, p.embedding as embedding, p.statement as statement, 
            p.date as date, p.url as url;
        '''
        with self.driver.session() as session:
            records, summary, keys = self.driver.execute_query(
                query,
                database_="neo4j",
            )
            statements = [p.data() for p in records]
        return statements

    def get_top10_cosine_vectors(self, query_id):
        query = '''USE neo4j 
        MATCH (n:Fake_Statement), (p:Fake_Statement) 
        WHERE n.id = $query_id and p.query IS NULL 
        WITH n, p, gds.similarity.cosine(n.embedding, p.embedding) AS similarity 
        RETURN p.id as id, ID(p) as intra_id, p.embedding as embedding, 
        p.statement as statement, p.date as date, p.url as url, similarity ORDER BY 
        similarity DESC LIMIT 10'''
        with self.driver.session() as session:
            records, summary, keys = self.driver.execute_query(
                query,
                database_="neo4j",
                query_id=query_id
            )
            statements = [p.data() for p in records]
        return statements

    def get_all_statements(self):
        query = '''USE neo4j 
                MATCH (p:Fake_Statement) 
                WHERE p.query IS NULL
                RETURN p.id as id, ID(p) as intra_id, p.embedding as embedding, 
                p.statement as statement'''
        with self.driver.session() as session:
            records, summary, keys = self.driver.execute_query(
                query,
                database_="neo4j",
            )
            statements = [p.data() for p in records]
        return statements



    def get_top_cosine_vectors(self, query_id):
        query = '''USE neo4j 
           MATCH (n:Fake_Statement), (p:Fake_Statement) 
           WHERE n.id = $query_id and p.query IS NULL 
           WITH n, p, gds.similarity.cosine(n.embedding, p.embedding) AS similarity 
           WHERE similarity > 0.8
           RETURN p.id as id, ID(p) as intra_id, p.embedding as embedding, 
           p.statement as statement, p.date as date, p.url as url, similarity ORDER BY 
           similarity DESC LIMIT 50'''
        with self.driver.session() as session:
            records, summary, keys = self.driver.execute_query(
                query,
                database_="neo4j",
                query_id=query_id
            )
            statements = [p.data() for p in records]
        if len(statements) < 10:
            return self.get_top10_cosine_vectors(query_id)
        return statements

    def get_mix_cosine_words(self, query_id, query_words, skip):
        query = '''USE neo4j 
           MATCH (n:Fake_Statement), (p:Fake_Statement) 
           WHERE n.id = $query_id and p.query IS NULL and p.words is not null
           WITH n, p, gds.similarity.cosine(n.embedding, p.embedding) AS cos_similarity,
               size(apoc.coll.intersection(p.words , $query_words)) AS matching_words, 
               size($query_words) as total_words
           WITH n, p, 
               round((cos_similarity + toFloat(matching_words) / toFloat(total_words) / 7), 2) as med_similarity,
               cos_similarity, toFloat(matching_words) / toFloat(total_words) as added_similarity,
               matching_words
           WITH n, p,  med_similarity, cos_similarity, added_similarity, matching_words,
               apoc.coll.max([added_similarity, med_similarity]) as similarity
            RETURN p.id as id, ID(p) as intra_id, matching_words,
               p.statement as statement, p.date as date, p.formatted_date as f_date,
                p.embedding as embedding, p.url as url,
               similarity, cos_similarity, added_similarity, p.words ORDER BY 
               similarity DESC, f_date DESC SKIP $skip LIMIT 50 
           '''
        with self.driver.session() as session:
            records, summary, keys = self.driver.execute_query(
                query,
                database_="neo4j",
                query_id=query_id,
                query_words=query_words,
                skip=skip
            )
            statements = [p.data() for p in records]
        return statements

    def get_node(self, node_id):
        query = '''USE neo4j 
                 MATCH (n) 
                 WHERE n.intra_id = $id
                 return n, labels(n) as type
                 '''
        with self.driver.session() as session:
           records, summary, keys = self.driver.execute_query(
               query,
               database_="neo4j",
               id=node_id,
           )
           statements = [p.data() for p in records]
        return statements

    def get_mix_cosine_similar_node(self, query_id, like_node_id, other_results_ids):
        query = '''USE neo4j 
              MATCH (n:Fake_Statement), (p:Fake_Statement)--(g) 
              WHERE n.id = $query_id and p.query IS NULL and not p.id in $other_ids and g.intra_id = $like_node_id
              WITH n, p, gds.similarity.cosine(n.embedding, p.embedding) AS cos_similarity,
                  size(apoc.coll.intersection(p.words , n.words)) AS matching_words, 
                  size(n.words) as total_words
              WITH n, p, 
                  round((cos_similarity + toFloat(matching_words) / toFloat(total_words) / 7), 2) as med_similarity,
                  cos_similarity, toFloat(matching_words) / toFloat(total_words) as added_similarity,
                  matching_words
              WITH n, p,  med_similarity, cos_similarity, added_similarity, matching_words,
                  apoc.coll.max([added_similarity, med_similarity]) as similarity
               RETURN p.id as id, ID(p) as intra_id, matching_words,
                  p.statement as statement, p.date as date, p.formatted_date as f_date,
                   p.embedding as embedding, p.url as url,
                  similarity, cos_similarity, added_similarity, p.words ORDER BY 
                  similarity DESC, f_date DESC LIMIT 3 
              '''
        with self.driver.session() as session:
            records, summary, keys = self.driver.execute_query(
                query,
                database_="neo4j",
                query_id=query_id,
                like_node_id=like_node_id,
                other_ids=other_results_ids
            )
            statements = [p.data() for p in records]
        # if len(statements) < 10:
        #     return self.get_top10_cosine_vectors(query_id)
        return statements

 # MATCH (n:Fake_Statement), (p:Fake_Statement)
 #           WHERE n.id = 69951 and p.query IS NULL and p.words is not null
 #           WITH n, p, gds.similarity.cosine(n.embedding, p.embedding) AS cos_similarity, size(apoc.coll.intersection(p.words , [ 'ukrain', 'evil'])) AS matching_words, size(['ukrain', 'evil']) as total_words
 #           WITH n, p, round((cos_similarity + toFloat(matching_words) / toFloat(total_words) / 7), 2) as med_similarity, cos_similarity, toFloat(matching_words) / toFloat(total_words) as added_similarity, matching_words
 #           WITH n, p,  med_similarity, cos_similarity, added_similarity, matching_words, apoc.coll.max([added_similarity, med_similarity]) as similarity
 #           RETURN p.id as id, ID(p) as intra_id, matching_words,
 #           p.statement as statement, p.date as date, p.formatted_date as f_date, similarity, cos_similarity, added_similarity, p.words ORDER BY
 #           similarity DESC, f_date DESC LIMIT 50
 #

    def get_statement_location(self, intra_id):
        query = '''
            USE neo4j
            MATCH (p:Fake_Statement)-[:HAS_LOCATION]-(g:Location)
            WHERE p.intra_id=$intra_id 
            RETURN g;
        '''
        with self.driver.session() as session:
            records, summary, keys = self.driver.execute_query(
                query,
                database_="neo4j",
                intra_id=intra_id
            )
            statements = [g.data()["g"]["location"] for g in records]
        if len(statements) > 0:
            return statements

        return ""

    def get_statement_channel(self, intra_id):
        query = '''
            USE neo4j
            MATCH (p:Fake_Statement)-[:HAS_CHANNEL]-(g:Channel)
            WHERE p.intra_id=$intra_id 
            RETURN g;
        '''
        with self.driver.session() as session:
            records, summary, keys = self.driver.execute_query(
                query,
                database_="neo4j",
                intra_id=intra_id
            )
            statements = [g.data()["g"]["name"] for g in records]
            if len(statements) > 0:
                return statements

        return ""

    def get_statement_language(self, intra_id):
        query = '''
            USE neo4j
            MATCH (p:Fake_Statement)-[:HAS_LANGUAGE]-(g:Language)
            WHERE p.intra_id=$intra_id 
            RETURN g;
        '''
        with self.driver.session() as session:
            records, summary, keys = self.driver.execute_query(
                query,
                database_="neo4j",
                intra_id=intra_id
            )
            statements = [g.data()["g"]["name"] for g in records]
            if len(statements) > 0:
                return statements

        return ""


    def simple_delete(self, id):
        # print('simple_delete')
        query = '''
                MATCH (p:Fake_Statement)
                WHERE ID(p) = $id and p.query=1
                detach delete p
                '''
        with self.driver.session() as session:
            records, summary, keys = self.driver.execute_query(
                query,
                database_="neo4j", id=id
            )
            # print(records)

    def drop_fake_statements_associates(self, id):
        querry = '''
        MATCH (p:Fake_Statement)
        WHERE ID(p) = $id and p.query=1
        WITH p
        OPTIONAL MATCH (p)-[r]-(allRelatedNodes)
        WITH p, allRelatedNodes
        Optional MATCH (allRelatedNodes)-[:HAS_KEYWORD]-(m)
        WITH COUNT(m) as nr_rel,  p, allRelatedNodes, ID(p) as pid, ID(allRelatedNodes) as allrel
        WHERE nr_rel < 2
        detach delete p, allRelatedNodes
        return pid, allrel
        '''
        with self.driver.session() as session:
            records, summary, keys = self.driver.execute_query(
                querry,
                database_="neo4j", id=id
            )
            print(records)
            print(summary)
            print(keys)
            statements = [p.data() for p in records]
            if len(statements) == 0:
                self.simple_delete(id)

    def del_similar_rel(self):
        querry = '''
        MATCH (n)-[r:SIMILAR]->()
        DELETE r
        '''
        with self.driver.session() as session:
            records, summary, keys = self.driver.execute_query(
                querry,
                database_="neo4j"
            )
            print(summary)

    def del_community_properties(self):
        querry = '''
        MATCH (a)
        REMOVE a.age
        '''
        with self.driver.session() as session:
            records, summary, keys = self.driver.execute_query(
                querry,
                database_="neo4j"
            )
            print(summary)


'''
States about communities

MATCH(p)  
WITH DISTINCT(p.community) as comm_id, COUNT(p) as Total_number
MATCH (q:Fake_Statement)
WHERE q.community = comm_id
RETURN comm_id, Total_number, COUNT(q) as Fake_S

Run Louvaine Algorithm

 USE news
       CALL gds.graph.project(
        'myGraph2',
        ['Fake_Statement', 'Entity', 'Person'],
        {
            HAS_KEYWORD: {
                orientation: 'UNDIRECTED'
            }
        }
        )
        
        
// First, aggregate by community and count the total nodes and Fake_Statement nodes
MATCH (p)
WITH DISTINCT(p.community) as comm_id, COUNT(p) as Total_number
MATCH (q:Fake_Statement)
WHERE q.community = comm_id
WITH comm_id, Total_number, COUNT(q) as Fake_S
// For each community, find the Fake_Statement with the most relationships
OPTIONAL MATCH (most_connected:Fake_Statement)-[r]-()
WHERE most_connected.community = comm_id
WITH comm_id, Total_number, Fake_S, most_connected, COUNT(r) as rel_count
ORDER BY rel_count DESC
WITH comm_id, Total_number, Fake_S, COLLECT(most_connected)[0..3] as Most_Connected_Statement
// For each community, find the top 3 entities with a has_keyword relationship
OPTIONAL MATCH ()-[:HAS_KEYWORD]->(e:Entity)
WHERE e.community = comm_id
WITH comm_id, Total_number, Fake_S, Most_Connected_Statement, e, COUNT(*) as keyword_count
ORDER BY keyword_count DESC
WITH comm_id, Total_number, Fake_S, Most_Connected_Statement, COLLECT(e.name)[0..3] as Top_Entities
RETURN comm_id, Total_number, Fake_S, Most_Connected_Statement, Top_Entities;


  MATCH (p)
            WITH DISTINCT(p.community) as comm_id, COUNT(p) as Total_number
            MATCH (q:Fake_Statement)
            WHERE q.community = comm_id
            WITH comm_id, Total_number, COUNT(q) as Fake_S
            // For each community, find the Fake_Statement with the most relationships
            OPTIONAL MATCH (most_connected:Fake_Statement)-[r]-()
            WHERE most_connected.community = comm_id
            WITH comm_id, Total_number, Fake_S, most_connected, COUNT(r) as rel_count
            ORDER BY rel_count DESC
            WITH comm_id, Total_number, Fake_S, COLLECT(most_connected) as statements
            RETURN comm_id, Total_number, Fake_S, statements;
'''
