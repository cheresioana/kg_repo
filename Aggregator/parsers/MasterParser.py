from knowledge_extraction.EntityExtractor import EntityExtractor
from parsers.BaseParser2 import BaseParser2


class MasterParser:
    def __init__(self):
        self.entity_extractor = EntityExtractor()

    def parse(self, payload):
        parser = BaseParser2()
        parsed = parser.parse(payload)
        return self.verify(parsed)

    """
    The verify method extracts relevant information like keywords, tags and entities
    It also normalizes the data (lowercase, camel case etc) depending on the field
    """

    def verify(self, final_object):
        # extract entities
        final_object['title_entities'] = self.entity_extractor.extract_entities(final_object['statement'])

        final_object['news_entities'] = self.entity_extractor.extract_entities(final_object['fake_news_content'])

        final_object['keywords'] = self.entity_extractor.get_keywords(final_object,
                                                                      final_object['title_entities'])

        final_object['tags'] = self.entity_extractor.get_tags_entities(final_object)

        # normalize text, so the fields which have the same information look the same
        final_object['languages'] = [lang.lower() for lang in final_object['languages']]
        final_object['spread_location'] = [loc.title() for loc in final_object['spread_location']]
        final_object['fake_news_source'] = [spread.lower() for spread in final_object['fake_news_source']]

        return final_object
