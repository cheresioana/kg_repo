from knowledge_extraction.EntityExtractor import EntityExtractor
from parsers.VeridicaParser import VeridicaParser


class MasterParser:
    def __init__(self):
        self.entity_extractor = EntityExtractor()

    def parse(self, payload):
        if payload['crawler_name'] == 'veridica':
            print('Veridica')
            parser = VeridicaParser()
            parsed = parser.parse(payload)
        return self.verify(parsed)

    def verify(self, payload):
        if not payload.final_object['entities']:
            payload.final_object['entities'] = self.entity_extractor.extract_entities(payload.final_object['statement'])
        print(payload.final_object)
        return payload
