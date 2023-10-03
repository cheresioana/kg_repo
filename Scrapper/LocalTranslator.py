from googletrans import Translator
from unidecode import unidecode
import time

'''
This translator uses google API to translate text in english. Because the sources may be in a variety of languages,
it must bring everything to english. If used raw, the translator gives a lot of times connection errors, and this wrapper class
hav in place the method of calling multiple times the translator in case of failure
'''
class LocalTranslator:
    def __init__(self):
        self.translator = Translator()


    def translate_call(self, text, src_lang='ro', dest_lang='en', retries=3, delay=5):
        if text is None or text == "":
            return ""
        for i in range(retries):
            try:
                translation = self.translator.translate(text, src=src_lang, dest=dest_lang)
                if translation is not None and translation.text is not None:
                    return translation.text
                else:
                    print(f"Received None from the API on attempt {i + 1}")

            except Exception as e:
                print(f"An error calling translation api Error:{e} For text: {text}")

            time.sleep(delay * (2 ** i))  # Exponential backoff

        raise Exception("Failed to translate text after multiple retries")
    def robust_translate(self, text, src_lang='ro', dest_lang='en', retries=3, delay=5):
        if text is None or text == "":
            return ""
        chunk_length = 5000
        chunks = [text[i:i+chunk_length] for i in range(0, len(text), chunk_length)]
        translated_chunks = []
        for chunk in chunks:
            translated_chunks.append(self.translate_call(chunk, src_lang='ro', dest_lang='en', retries=3, delay=5))
        return ''.join(translated_chunks)

