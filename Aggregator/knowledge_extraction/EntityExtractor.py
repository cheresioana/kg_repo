import pandas as pd
import spacy
from spacy import displacy

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
