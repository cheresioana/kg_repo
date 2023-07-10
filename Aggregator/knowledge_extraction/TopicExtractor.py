import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
from gensim import corpora
from gensim.models.ldamodel import LdaModel

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

class TopicExtractor():
    def __init__(self, ):
        self.stop = set(stopwords.words('english'))
        self.exclude = set(string.punctuation)
        self.lemma = WordNetLemmatizer()

    def clean(self, doc):
        stop_free = " ".join([i for i in doc.lower().split() if i not in self.stop])
        punc_free = ''.join(ch for ch in stop_free if ch not in self.exclude)
        normalized = " ".join(self.lemma.lemmatize(word) for word in punc_free.split())
        return normalized

    def extract_topic(self, statement, num_topics = 2):
        cleaned_texts = [self.clean(doc).split() for doc in statement]

        # Preparing Document-Term Matrix
        dictionary = corpora.Dictionary(cleaned_texts)
        doc_term_matrix = [dictionary.doc2bow(doc) for doc in cleaned_texts]

        # Running LDA Model
        ldamodel = LdaModel(doc_term_matrix, num_topics=num_topics, id2word=dictionary, passes=50)

        print(ldamodel.print_topics(num_topics=num_topics, num_words=5))
