from datetime import date


class DataObject:
    def __init__(self, crawler_name='veridica', crawler_origin='https://www.veridica.ro/baza-de-date'):
        self.crawler_name = crawler_name
        self.statement = ''
        self.date = ''
        self.spread_country = ''
        self.fake_news_source = ''
        self.debunking_argument = ''
        self.raw_page = ''
        self.debunking_link = ''
        self.crawler_origin = crawler_origin
        self.crawled_date = date.today()
        self.narrative = []

    def __str__(self):
        return f"""DataObject(
    crawler_name={self.crawler_name},
    statement={self.statement},
    date={self.date},
    spread_country={self.spread_country},
    fake_news_source={self.fake_news_source},
    debunking_argument={self.debunking_argument},
    raw_page={self.raw_page[:100]}...,
    debunking_link={self.debunking_link},
    crawler_origin={self.crawler_origin},
    narrative={self.narrative})"""

    def json_encoder(self):
        return {
            'crawler_name': self.crawler_name,
            'statement': self.statement,
            'date': self.date,
            'spread_country': self.spread_country,
            'fake_news_source': self.fake_news_source,
            'debunking_argument': self.debunking_argument,
            'raw_page': str(self.raw_page),
            'debunking_link': self.debunking_link,
            'crawler_origin': self.crawler_origin,
            'narrative': self.narrative}
