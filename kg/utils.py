from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re
from constanst import MAX_TOKENS
import nltk
import spacy
import pytextrank
stop_words = set(stopwords.words('english'))
nltk.download('punkt')
nltk.download('stopwords')


def clean_text(my_text):
    print("Clean text")
    print(my_text)
    my_text = my_text.lower()
    my_text = re.sub(r'[^a-z0-9 ]', '', my_text)
    # lowercasing all the text
    tokens = word_tokenize(my_text)#my_text.split()
    # tokenizing
    tokens = [word for word in tokens if word not in stop_words]
    # stemming
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(token) for token in tokens]
    # tokens = [token for token in tokens if len(token) > 2]
    final_text = ' '.join(tokens)
    print(final_text)
    if len(final_text) < MAX_TOKENS:
        return final_text
    return final_text[:MAX_TOKENS]


def get_clean_text_tokens(my_text):
    # print("Clean text")
    # print(my_text)
    my_text = my_text.lower()
    my_text = re.sub(r'[^a-z0-9 ]', '', my_text)
    # lowercasing all the text
    tokens = word_tokenize(my_text)#my_text.split()
    # tokenizing
    tokens = [word for word in tokens if word not in stop_words]
    # stemming
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(token) for token in tokens]


    if len(tokens) < 10:
        return tokens

    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("textrank")
    processed = nlp(my_text)
    keywords = [p.text for p in processed._.phrases]
    tokens = [stemmer.stem(t) for token in keywords for t in token.split() if t not in stop_words]
    tokens = list(set(tokens))
    return tokens[:10]
