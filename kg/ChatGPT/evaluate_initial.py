import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

if __name__=='__main__':
    df1 = pd.read_csv('initial_debunks.csv')
    df2 = pd.read_csv('test_entries.csv')
    df3 = pd.read_csv('initial_debunks_fine_tune.csv')

    cos_1 = []
    cos_2 = []

    for index, row in df1.iterrows():
        id_s = row['id']
        element = df2[df2['id'] == id_s]
        full_exp = str(element['full_explanation'].iloc[0])

        element2 = df3[df3['id'] == id_s]
        full_exp2 = str(element2['debunk'].iloc[0])

        #print(full_exp)
        vectorizer = TfidfVectorizer()

        # Fit and transform the documents
        tfidf_matrix = vectorizer.fit_transform([full_exp, row['debunk'], full_exp2])
        cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix).flatten()
        cos_1.append(cosine_similarities[1])
        cos_2.append(cosine_similarities[2])
        # Print the cosine similarities
        print(cosine_similarities)

    print("The average is:" + str(sum(cos_1) / len(cos_1)))
    print("The average is:" + str(sum(cos_2) / len(cos_2)))



