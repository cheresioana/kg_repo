import json
import string

import pandas as pd
import spacy
import pytextrank
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

'''import nltk
nltk.download('punkt')
nltk.download('stopwords')'''

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
    #print(ents)
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("textrank")
    processed = nlp(row['statement'] + row['fake_news_content'])
    keywords = [p.text for p in processed._.phrases]

    #print(keywords)

    result = [item for item in keywords if item not in ents]
    #print(result)
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
        #result2.append(filtered_text)


    return entities

if __name__ == '__main__':
    df = pd.read_csv('data.csv')
    connector = NeoConnector()
    '''connector.get_similar(417)
    exit(0)
    #print(df.iloc[23])
    row = df.iloc[48]
    connector.set_similarity()
    connector.select_communities()'''

    '''entities = enrich_by_nlp(row)
    print(row)
    print(entities)
    connector.insert_statement(row)
    connector.insert_statement_entities(row, entities)'''
    for index, row in df.iterrows():
        # print(f"Enriching {topic} documents")
        #print(row['statement'])
        title_entities = eval(row['title_entities'])
        keywords = get_keywords(row, title_entities)
        #print(keywords)

        #keywords = [{'name': clean_keyword(x.text), 'rank': x.rank}]
        #print(keywords)

        #news_entities = eval(row['news_entities'])
        connector.insert_statement(row)
        connector.insert_statement_entities(row['id'], title_entities)
        connector.insert_statement_entities(row['id'], keywords)
        #exit(0)
        #connector.insert_statement_entities(row, news_entities)
    #connector.set_similarity()