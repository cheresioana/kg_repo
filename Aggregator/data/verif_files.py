import pandas as pd
import os


def print_stats(df):
    print(f'Shape: {df.shape}')
    # print(f'Columns: {df.columns}')
    sample = df[['statement', 'spread_location', 'fake_news_source', 'tags', 'languages']].head(1)
    # print(f'Sample: {sample }')
    rows_nan_statement = df[df['statement'].isna()]
    rows_empty_statement = df[df['statement'] == '']
    print(f'Nan in statement {rows_nan_statement.shape[0]}, empty statement {rows_empty_statement.shape[0]}')
    rows_nan_date = df[df['date'].isna()]
    rows_empty_date = df[df['date'] == '']
    print(f'Nan in date {rows_nan_date.shape[0]}, empty date {rows_empty_date.shape[0]}')
    rows_nan_location = df[df['spread_location'].isna()]
    rows_empty_location = df[df['spread_location'] == "['']"]
    print(f'Nan in location {rows_nan_location.shape[0]}, empty location {rows_empty_location.shape[0]}')
    rows_nan_source = df[df['fake_news_source'].isna()]
    rows_empty_source = df[
        (df['fake_news_source'] == '') | (df['fake_news_source'] == "[]") | (df['fake_news_source'] == "['']")]
    print(f'Nan in source {rows_nan_source.shape[0]}, empty source {rows_empty_source.shape[0]}')
    rows_nan_debunk = df[df['debunking_link'].isna()]
    rows_empty_debunk = df[df['debunking_link'] == '']
    print(f'Nan in debunk_link {rows_nan_debunk.shape[0]}, empty debunk {rows_empty_debunk.shape[0]}')
    rows_nan_languages = df[df['languages'].isna()]
    rows_empty_languages = df[
        (df['languages'] == '') | (df['languages'] == "[]") | (df['languages'] == "['']")]
    print(f'Nan in languages {rows_nan_languages.shape[0]}, empty languages {rows_empty_languages.shape[0]}')
    print('\n\n')


'''
This script takes all the csv files from the current folder and prints some overall info about them.
It verifies how many entries have missing 
    (a) statement,
    (b) date,
    (c) location,
    (d) source,
    (e) debunk link,
    (f) languages
'''

if __name__ == '__main__':
    pd.set_option('display.max_rows', 500)  # Example to display up to 500 rows
    pd.set_option('display.max_columns', 20)  # Example to display up to 20 columns
    pd.set_option('display.max_colwidth', None)  # Display the full width of each column

    df_final = None
    for filename in os.listdir('.'):
        if filename.endswith('.csv'):
            print(filename)
            df = pd.read_csv(filename)
            print_stats(df)
            if df_final is None:
                df_final = df
            else:
                df_final = pd.concat([df_final, df], axis=0)

    print(f'Final dataset {df_final.shape}')
    df_final.to_csv('all_data.csv', index=False)
