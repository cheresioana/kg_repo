from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk

nltk.download('punkt')
nltk.download('stopwords')

#from constanst import MAX_TOKENS
MAX_TOKENS = 1500
stop_words = set(stopwords.words('english'))


def clean_text(my_text):

    my_text = my_text.lower()
    # lowercasing all the text
    tokens = my_text.split()
    # tokenizing
    tokens = [word for word in tokens if word not in stop_words]
    # stemming
    #stemmer = PorterStemmer()
    #tokens = [stemmer.stem(token) for token in tokens]
    # tokens = [token for token in tokens if len(token) > 2]
    final_text = ' '.join(tokens)
    #if len(final_text) < MAX_TOKENS:
    return final_text
    #return final_text[:MAX_TOKENS]
