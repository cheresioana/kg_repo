from TopicExtractor import TopicExtractor
from knowledge_extraction.EntityExtractor import EntityExtractor


def topic_tests():
    topic_extraction = TopicExtractor()
    texts = [
        "The fox jumps over the lazy dog.",
        "I love to play football.",
        "The pizza tastes really good."
    ]
    topic_extraction.extract_topic(texts)

def entities_ext():
    enitiy_extractor = EntityExtractor()
    enitiy_extractor.extract_entities('Fake News Monitor No. 51: Russian propagandists want genocide')

if __name__=='__main__':
    entities_ext()
