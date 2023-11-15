import json
import os
import string
import sys

import pandas as pd
import spacy
import pytextrank
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import logging
'''import nltk
nltk.download('punkt')
nltk.download('stopwords')'''
from urllib.parse import urlparse
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Neo4JConnector.NeoConnector import NeoConnector


def enrich_by_nlp(row):
    nlp = spacy.load("en_core_web_sm")

    processed = nlp(row['statement'])
    entities = {}
    for en in processed.ents:
        if en.label_ not in entities:
            entities[en.label_] = list()
        entities[en.label_].append(en.text.replace("\'s", "").strip())
    return entities


def clean_keyword(keyword):
    keywords = [word.lower() for word in keyword]

    # Remove punctuation
    keywords = [''.join(ch for ch in word if (ch not in string.punctuation) or len(ch) > 3) for word in keywords]

    return keywords


def get_keywords(row, title_entities):
    ents = title_entities.values()
    ents = [item for sublist in ents for item in sublist]
    entities = {}
    # print(ents)
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("textrank")
    processed = nlp(row['statement'] + row['fake_news_content'])
    keywords = [p.text for p in processed._.phrases]

    # print(keywords)

    result = [item for item in keywords if item not in ents]
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


def populate():
    df = pd.read_csv('../data/data_with_embeddings.csv')
    connector = NeoConnector()
    i = 0

    for index, row in df.iterrows():
        if pd.isna(row['statement']):
            logging.error(f"Missing statement {row}")
            continue
        title_entities = eval(row['title_entities'])
        keywords = eval(row['keywords'])
        tags = eval(row['tags'])
        print(row)
        row['embedding'] = eval(row['embedding'])
        if pd.isna(row['date']):
            row["date"] = ""

        record_id = connector.insert_statement(row)
        connector.insert_statement_entities(record_id, title_entities)
        connector.insert_statement_entities(record_id, keywords)
        connector.insert_statement_entities(record_id, tags)

        spread_locations = eval(row['spread_location'])
        for location in spread_locations:
            connector.insert_location(record_id, location)

        fake_news_sources = eval(row['fake_news_source'])
        for source in fake_news_sources:
            parsed_url = urlparse(source)
            base_url = parsed_url.netloc
            connector.insert_channel(record_id, base_url)

        #connector.insert_statement_entities(row['id'], keywords)
        print(i)
        i = i + 1
        #if i > 30:
        #    return 0

        #exit(0)
        # connector.insert_statement_entities(row, news_entities)
    # connector.set_similarity()

if __name__ == '__main__':
    populate()