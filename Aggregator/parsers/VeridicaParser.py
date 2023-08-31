import time

from parsers.BaseParser2 import BaseParser2
from googletrans import Translator
from unidecode import unidecode

class VeridicaParser(BaseParser2):
    def __init__(self):
        BaseParser2.__init__(self)
        self.translator = Translator()

    def robust_translate(self, text, src_lang='ro', dest_lang='en', retries=3, delay=5):
        if text is None or text == "":
            return ""
        for i in range(retries):
            try:
                translation = self.translator.translate(text, src=src_lang, dest=dest_lang)
                if translation is not None and translation.text is not None:
                    return translation.text
                else:
                    print(f"Received None from the API on attempt {i+1}")

            except Exception as e:
                print(f"An error calling translation api {e} {text}")

            time.sleep(delay * (2 ** i))  # Exponential backoff

        raise Exception("Failed to translate text after multiple retries")

    def parse(self, payload):
        #translator =
        self.final_object['owner'] = 'veridica'
        if payload['statement'] is not None:
            self.final_object['statement'] = self.robust_translate(payload['statement'])
        else:
            return None
        if payload['debunking_argument'] is not None:
            self.final_object['full_explanation'] = ' '.join([self.robust_translate(unidecode(x)) for x in payload['debunking_argument']])
        else:
            return None

        if not (payload.get('verdict') is None):
            self.final_object['verdict'] = payload['verdict']
        if not (payload.get('narrative') is None):
            self.final_object['narrative'] = [self.robust_translate(unidecode(x)) for x in payload['narrative']]
        if not (payload.get('speaker') is None):
            self.final_object['speaker'] = payload['speaker']
        if not (payload.get('speaker_job_title') is None):
            self.final_object['speaker_job_title'] = self.robust_translate(payload['speaker_job_title'])
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
            self.final_object['fake_news_content'] = self.robust_translate(payload['fake_news_content'])
        if not (payload.get('summary_explanation') is None):
            self.final_object['summary_explanation'] = self.robust_translate(payload['summary_explanation'])

        return self
