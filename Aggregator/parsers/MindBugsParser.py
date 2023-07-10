import pandas as pd
from googletrans import Translator
import numpy as np
from parsers.BaseParser import BaseParser


class MindBugsParser(BaseParser):
    def __init__(self, file_name):
        df = pd.read_csv(file_name)
        BaseParser.__init__(self, df)

    def parse_dataset(self):
        self.set_statement(self.target_df["statement_en"])
        self.set_subject(self.parse_subjects(self.target_df["subject_en"]))
        self.set_verdict_column(self.target_df["verdict"].str.lower())
        self.set_speaker(self.target_df["speaker"])

        self.set_summary(self.target_df["summary_explanation_en"])
        self.set_explanation(self.target_df["full_explanation_en"])
        media_channel = self.target_df['name'] \
            .replace({'Source is not on social media': 'other'}) \
            .str.lower()
        self.set_media_channel(media_channel)
        self.set_likes(self.target_df["likes"])
        self.set_comments(self.target_df["comments"])
        self.set_shares(self.target_df["shares"])
        self.set_news_sources(self.target_df["news_source"])
        self.set_debunk_sources(self.target_df["explain_sources"])
        self.set_journalist(self.target_df["user_id"])
        self.set_debunk_date(self.target_df["created_date"])
        self.set_location(self.target_df["location"])

        # job title of the speaker is translated
        translator = Translator()

        column = self.target_df["job_title"]
        col = column.apply(lambda x: translator.translate(x, src='ro').text if (x and not pd.isna(x)) else '')
        print(col)
        self.set_speaker_job(col)

        # create the debunk link
        column = self.target_df["fakenews_id"]
        col = column.apply(lambda x: 'https://mindbugs.ro/debunk/viewDebunk/' + str(x))
        self.set_debunk_link(col)
