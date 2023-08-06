import pandas as pd
import re

class BaseParser:
    def __init__(self, df):
        self.target_df = df
        self.__final_df = pd.DataFrame(columns=['statement', 'narrative',
                                              'verdict',
                                              # can be: true, mostly-true, half-true, 'mostly-false', 'false'
                                              'speaker', 'speaker_job_title',
                                              # the person to whom is attributed the statement
                                              'summary_explanation', 'full_explanation',
                                              'media_channel',  # facebook, twitter, instagram, tiktok, other
                                              'likes', 'comments', 'shares',
                                              'news_sources', 'debunk_sources',  # links separated through ;
                                              'journalist_id', 'debunk_date',
                                              'subject', 'location',
                                              'owner', 'debunk_link', 'fake_news_content'
                                              ])

    def set_owner(self, owner):
        self.__final_df['owner'] = owner

    def parse_subjects(self, column):
        '''
        Output: a column for the target dataset that contains the subjects separated by comma
        This functions performs some general data cleaning for the subject column of the dataset.
        It includes: lowercase, deletes extra spaces, removes unwanted separators
        '''
        column = column.str.lower()
        column = column.str.strip()
        column = column.str.replace('[-_/&]', ',', regex=True)
        column = column.str.replace(',\s+', ',', regex=True)
        column = column.str.replace('\s+,', ',', regex=True)
        return column

    def check_final_dataframe(self):
        return True

    def get_target_df(self):
        return self.target_df

    def set_verdict_column(self, column):
        column = column.str.replace('\s+', '', regex=True)
        column = column.apply(str.lower)
        assert column.isin(['true', 'mostly-true', 'half-true', 'mostly-false', 'false']).all()
        self.__final_df["verdict"] = column

    def set_media_channel(self, column):
        assert column.isin(['facebook', 'twitter', 'instagram', 'tiktok', 'other']).all()
        self.__final_df["media_channel"] = column

    def set_statement(self, column):
        self.__final_df['statement'] = column

    def set_subject(self, column):
        self.__final_df['subject'] = column

    def set_speaker(self, column):
        self.__final_df['speaker'] = column

    def set_speaker_job(self, column):
        self.__final_df['speaker_job_title'] = column

    def set_summary(self, column):
        self.__final_df['summary_explanation'] = column

    def set_explanation(self, column):
        self.__final_df['full_explanation'] = column

    def set_likes(self, column):
        self.__final_df['likes'] = column

    def set_comments(self, column):
        self.__final_df['comments'] = column

    def set_shares(self, column):
        self.__final_df['shares'] = column

    def set_news_sources(self, column):
        links = column.str.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$/\-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        col = links.apply(lambda x: ';'.join(map(str, x)))
        self.__final_df['news_sources'] = col

    def set_debunk_sources(self, column):
        links = column.str.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$/\-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        col = links.apply(lambda x: ';'.join(map(str, x)))
        self.__final_df['debunk_sources'] = col

    def set_journalist(self, column):
        unique = column.unique()
        new_values = [anonymize_nr for anonymize_nr in range(0, len(unique))]
        column = column.replace(unique, new_values)
        self.__final_df['journalist_id'] = column

    def set_debunk_date(self, column):
        print(column)
        column = pd.to_datetime(column)
        print(column.dt.strftime('%d/%m/%Y'))
        self.__final_df['debunk_date'] = column.dt.strftime('%d/%m/%Y').astype(str)

    def set_debunk_link(self, column):
        self.__final_df['debunk_link'] = column

    def set_location(self, column):
        self.__final_df['location'] = column

    def get_final_df(self):
        assert self.__final_df['owner'].notnull().all()
        assert self.__final_df['statement'].notnull().all()
        return self.__final_df

