from knowledge_extraction.EntityExtractor import EntityExtractor
from parsers.VeridicaParser import VeridicaParser


class MasterParser:
    def __init__(self):
        self.entity_extractor = EntityExtractor()

    def parse(self, payload):
        if payload['crawler_name'] == 'veridica':
            #print('Veridica')
            parser = VeridicaParser()
            parsed = parser.parse(payload)
        return self.verify(parsed)

    def verify(self, payload):
        if not payload.final_object['title_entities']:
            payload.final_object['title_entities'] = self.entity_extractor.extract_entities(payload.final_object['statement'])
        if not payload.final_object['news_entities']:
            payload.final_object['news_entities'] = self.entity_extractor.extract_entities(payload.final_object['fake_news_content'])
        if not payload.final_object['keywords']:
            payload.final_object['keywords'] = self.entity_extractor.get_keywords(payload.final_object,
                                                                                  payload.final_object['title_entities'])
        #print(payload.final_object)
        return payload
