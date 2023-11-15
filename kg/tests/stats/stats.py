import pandas as pd
from collections import Counter
import nltk
from nltk.corpus import stopwords

from textblob import TextBlob
nltk.download('stopwords')


def get_common_words(all_statements):
    words = all_statements.split()

    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word not in stop_words]

    # Count the frequency of each word
    word_count = Counter(filtered_words)

    # Find the most frequent words
    most_frequent_words = word_count.most_common(8)
    print(most_frequent_words)


def get_most_common_words(df):
    print('Most common words in statements')
    get_common_words(' '.join(df['statement'].astype(str)))

    print('Most common words in fake news text')
    get_common_words(' '.join(df['fake_news_content'].astype(str)))

    print('Most common words in explanations')
    get_common_words(' '.join(df['summary_explanation'].astype(str)))
    # all_statements = ' '.join(df['statement'])


def get_most_common_entities(df):
    entity_type_counter = Counter()
    entity_value_counter = Counter()

    for index, row in df.iterrows():
        entities = eval(row['title_entities'])
        for entity_type, entity_values in entities.items():
            entity_type_counter[entity_type] += len(entity_values)
            for value in entity_values:
                entity_value_counter[value] += 1

    # Find the most common entity types
    most_common_types = entity_type_counter.most_common(10)

    # Find the most common entity values
    most_common_values = entity_value_counter.most_common(20)

    # Print results
    print('Most Common Entity Types:', most_common_types)
    print('Most Common Entity Values:', most_common_values)

def find_sentiments(df):
    # Initialize counters for sentiment
    sentiment_counter = Counter()
    df['sentiment'] = df['statement'].astype(str).apply(lambda x: TextBlob(x).sentiment.polarity)

    # Categorize sentiment as Positive, Negative or Neutral
    df['sentiment_category'] = df['sentiment'].apply(
        lambda x: 'Positive' if x > 0 else ('Negative' if x < 0 else 'Neutral')
    )

    # Count how many rows have each type of sentiment


    # Update sentiment counter
    sentiment_counter.update(df['sentiment_category'].tolist())

    # Print the DataFrame with the sentiment and sentiment category

    # Print the count using Counter (Alternative approach)
    print("Sentiment Counter For Statement:", sentiment_counter)


    sentiment_counter = Counter()
    df['sentiment'] = df['fake_news_content'].astype(str).apply(lambda x: TextBlob(x).sentiment.polarity)

    # Categorize sentiment as Positive, Negative or Neutral
    df['sentiment_category'] = df['sentiment'].apply(
        lambda x: 'Positive' if x > 0 else ('Negative' if x < 0 else 'Neutral')
    )

    # Count how many rows have each type of sentiment
    sentiment_counts = df['sentiment_category'].value_counts()

    # Update sentiment counter
    sentiment_counter.update(df['sentiment_category'].tolist())

    # Print the DataFrame with the sentiment and sentiment category

    print("Sentiment Counter Fake news:", sentiment_counter)
    df.drop('sentiment_category', axis=1)

    df['sentiment'] = df['summary_explanation'].astype(str).apply(lambda x: TextBlob(x).sentiment.polarity)

    # Categorize sentiment as Positive, Negative or Neutral
    df['sentiment_category'] = df['sentiment'].apply(
        lambda x: 'Positive' if x > 0 else ('Negative' if x < 0 else 'Neutral')
    )

    # Count how many rows have each type of sentiment
    sentiment_counts = df['sentiment_category'].value_counts()

    # Update sentiment counter
    sentiment_counter.update(df['sentiment_category'].tolist())

    # Print the DataFrame with the sentiment and sentiment category


    # Print the count using Counter (Alternative approach)
    print("Sentiment Counter summary explanation:", sentiment_counter)


def get_attacked_countries(df):
    print(df['spread_location'].value_counts())

if __name__ == '__main__':
    df = pd.read_csv('../../data/data2.csv')
    print("General Info")
    print(df.shape)
    # missing_values = df.isna().sum()
    # for column, missing_count in missing_values.items():
    #     print(f"Column {column} has {missing_count} missing values.")
    # #print(df.columns)
    #
    # get_most_common_words(df)
    # get_most_common_entities(df)
    #
    # get_attacked_countries(df)
    # find_sentiments(df)
    year = 2023
    while year > 2015:

        df_new = df[df['date'].str.contains('.'+str(year) + '$')]
        print(year)
        print(df_new.shape)
        get_most_common_words(df_new)
        year = year - 1

