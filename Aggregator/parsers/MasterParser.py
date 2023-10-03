from knowledge_extraction.EntityExtractor import EntityExtractor
from parsers.BaseParser2 import BaseParser2


class MasterParser:
    def __init__(self):
        self.entity_extractor = EntityExtractor()

    def parse(self, payload):
        parser = BaseParser2()
        parsed = parser.parse(payload)
        return self.verify(parsed)

    def verify(self, final_object):

        final_object['title_entities'] = self.entity_extractor.extract_entities(final_object['statement'])

        final_object['news_entities'] = self.entity_extractor.extract_entities(final_object['fake_news_content'])

        final_object['keywords'] = self.entity_extractor.get_keywords(final_object,
                                                                                  final_object['title_entities'])
        #print(payload.final_object)
        return final_object
