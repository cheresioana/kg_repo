import os
import openai
import pandas as pd

from utils import clean_text
from openai.embeddings_utils import get_embedding, cosine_similarity

class OpenAIEmbeddingWrapper:
    def __init__(self):
        openai.api_key = os.environ.get('OPENAI_API_KEY')

    def init_embeddings_from_csv(self, file_name='data/data2.csv'):
        df = pd.read_csv(file_name)
        embedding_model = "text-embedding-ada-002"
        df = df.dropna(subset=['statement'])
        df['fake_news_content'].fillna('', inplace=True)
        df["combined_text"] = df['statement'] + " " + df["fake_news_content"]
        print(df["combined_text"])
        df['clean_combined_text'] = df["combined_text"].apply(clean_text)

        df["embedding"] = df['clean_combined_text'].apply(lambda x: get_embedding(x, engine=embedding_model))
        df.to_csv("data/data_with_embeddings.csv")

    def search_vector_space_dataframe(self, df, query, n=3):
        clean_query = clean_text(query)
        query_embedding = get_embedding(
            clean_query,
            engine="text-embedding-ada-002"
        )
        df["similarity"] = df.embedding.apply(lambda x: cosine_similarity(x, query_embedding))
        results = (
            df.sort_values("similarity", ascending=False)
            .head(n)
        )
        return results
    def get_embedding(self, query:str):
        query_embedding = get_embedding(
            query,
            engine="text-embedding-ada-002"
        )
        return query_embedding