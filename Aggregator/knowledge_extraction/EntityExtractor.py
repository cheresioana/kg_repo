import pandas as pd
import spacy
from spacy import displacy

class EntityExtractor():
    def __init__(self, ):
        self.NER = spacy.load("en_core_web_sm")

    def extract_entities(self, statement):
        entities = self.NER(statement)
        text_ents = [e.text for e in entities.ents]
        return text_ents
