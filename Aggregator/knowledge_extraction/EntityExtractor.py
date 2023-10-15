import pandas as pd
import spacy
from spacy import displacy

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pytextrank
import nltk

nltk.download('punkt')
nltk.download('stopwords')


class EntityExtractor():
    def __init__(self, ):
        self.NER = spacy.load("en_core_web_sm")

    def extract_entities(self, text):
        nlp = self.NER

        processed = nlp(text)
        entities = {}
        for en in processed.ents:
            if en.label_ not in entities:
                entities[en.label_] = list()
            entities[en.label_].append(en.text.replace("\'s", "").strip())
        return entities

    def extract_entities_simple(self, statement):
        entities = self.NER(statement)
        text_ents = [e.text for e in entities.ents]
        return text_ents

    def get_keywords(self, row, title_entities):
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

    def get_tags_entities(self, data_object):
        result = {'keywords': []}
        source = data_object['tags']
        for element in source:
            print(element)
            entities = self.extract_entities(element)
            print(entities)
            if not entities and element not in result['keywords']:
                result['keywords'].append(element)
            for en in entities.keys():
                if en not in result.keys():
                    result[en] = list()
                for entity in entities[en]:
                    if entity not in result[en]:
                        result[en].append(entity)
        return result
