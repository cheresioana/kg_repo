from datetime import datetime
import json


class DataObject:

    def __init__(self):
        self.crawler_name = ''
        self.statement = ''
        self.narrative = []
        self.verdict = False
        self.debunking_argument = ''
        self.debunking_link = ''
        self.crawler_origin = ''
        self.crawled_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.tags = []

        self.fake_news_content = ''
        self.summary_explanation = ''

        self.speaker = ''
        self.speaker_job_title = ''
        # the person to whom is attributed the statement

        self.media_channel = ''
        self.likes = -1
        self.comments = -1
        self.shares = -1
        # where the fake news was published Instagram, Twitter, Facebook

        self.date = ''
        self.journalist_name = ''
        self.spread_location = []
        self.fake_news_source = []
        self.debunk_sources = []
        self.topic = ''

    def init_from_json(self, j):
        self.__dict__ = json.loads(j)

    def __str__(self):
        return f"""DataObject(
    crawler_name={self.crawler_name},
    statement={self.statement},
    date={self.date},
    spread_location={self.spread_location},
    fake_news_source={self.fake_news_source},
    debunking_link={self.debunking_link},
    crawler_origin={self.crawler_origin},
    crawled_date={self.crawled_date},
    narrative={self.narrative},
    verdict={self.verdict},
    speaker={self.speaker},
    speaker_job_title={self.speaker_job_title},
    media_channel={self.media_channel},
    likes={self.likes},
    comments={self.comments},
    shares={self.shares},
    journalist_name={self.journalist_name},
    debunk_sources={self.debunk_sources},
    topic={self.topic},
    tags={self.tags},
    debunking_argument={self.debunking_argument},
    fake_news_content={self.fake_news_content},
    summary_explanation={self.summary_explanation},
    )"""

    def json_encoder(self):
        return {
            'crawler_name': self.crawler_name,
            'statement': self.statement,
            'date': self.date,
            'spread_location': self.spread_location,
            'fake_news_source': self.fake_news_source,

            'debunking_link': self.debunking_link,
            'crawler_origin': self.crawler_origin,
            'crawled_date': self.crawled_date,
            'narrative': self.narrative,

            'verdict': self.verdict,
            'speaker': self.speaker,
            'speaker_job_title': self.speaker_job_title,
            'media_channel': self.media_channel,
            'likes': self.likes,
            'comments': self.comments,
            'shares': self.shares,
            'journalist_name': self.journalist_name,
            'debunk_sources': self.debunk_sources,
            'topic': self.topic,
            'fake_news_content': self.fake_news_content,
            'summary_explanation': self.summary_explanation,
            'debunking_argument': self.debunking_argument,
        }
