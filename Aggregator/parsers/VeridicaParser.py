from parsers.BaseParser2 import BaseParser2
from googletrans import Translator
from unidecode import unidecode

class VeridicaParser(BaseParser2):
    def __init__(self):
        BaseParser2.__init__(self)

    def parse(self, payload):
        translator = Translator()
        self.final_object['owner'] = 'veridica'
        if payload['statement'] is not None:
            self.final_object['statement'] = translator.translate(payload['statement'], src='ro').text
        else:
            return None
        if payload['debunking_argument'] is not None:
            self.final_object['full_explanation'] = ' '.join([translator.translate(unidecode(x), src='ro').text for x in payload['debunking_argument']])
        else:
            return None

        if not (payload.get('verdict') is None):
            self.final_object['verdict'] = payload['verdict']
        if not (payload.get('narrative') is None):
            self.final_object['narrative'] = [translator.translate(unidecode(x), src='ro').text for x in payload['narrative']]
        if not (payload.get('speaker') is None):
            self.final_object['speaker'] = payload['speaker']
        if not (payload.get('speaker_job_title') is None):
            self.final_object['speaker_job_title'] = translator.translate(payload['speaker_job_title'], src='ro').text
        if not (payload.get('media_channel') is None):
            self.final_object['media_channel'] = payload['media_channel']
        if not (payload.get('fake_news_source') is None):
            self.final_object['fake_news_source'] = payload['fake_news_source']
        if not (payload.get('debunking_link') is None):
            self.final_object['debunk_sources'] = payload['debunking_link']
            self.final_object['debunk_link'] = payload['debunking_link']
        if not (payload.get('date') is None):
            self.final_object['debunk_date'] = payload['date']
        if not (payload.get('spread_country') is None):
            self.final_object['spread_location'] = payload['spread_country']
        if not (payload.get('fake_news_content') is None):
            self.final_object['fake_news_content'] = translator.translate(payload['fake_news_content'],
                                                                              src='ro').text

        return self
