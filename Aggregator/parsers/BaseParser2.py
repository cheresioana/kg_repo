import itertools

import pandas as pd
import re


class BaseParser2:
    def __init__(self):
        self.final_object = {
            'id': BaseParser2._get_next_id(),
            'statement': '',
            'narrative': [],
            # can be: true, mostly-true, half-true, 'mostly-false', 'false'
            'verdict': False,
            'topics': [],
            'title_entities': [],
            'news_entities': [],
            'speaker': '',
            'speaker_job_title': '',
            # the person to whom is attributed the statement
            'media_channel': '',  # facebook, twitter, instagram, tiktok, other
            'likes': '',
            'comments': '',
            'shares': '',
            'fake_news_source': '',
            'debunk_sources': '',  # links separated through ;
            'journalist': '',
            'debunk_date': '',
            'subject': '',
            'spread_location': '',
            'owner': '',
            'debunk_link': '',
            'summary_explanation': '',
            'full_explanation': '',
            'fake_news_content': ''

        }

    @staticmethod
    def _get_next_id():
        try:
            with open('next_id.txt', 'r') as f:
                next_id = int(f.read())
        except FileNotFoundError:
            next_id = 0

        with open('next_id.txt', 'w') as f:
            f.write(str(next_id + 1))

        return next_id

    def parse(self, pyload):
        pass
