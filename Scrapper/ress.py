from bs4 import BeautifulSoup
from unidecode import unidecode

from LocalTranslator import LocalTranslator
import re


def extract_text_between_strings(html, x, y):
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text().lower()  # get all text, discarding tags
    try:
        start = text.index(x) + len(x)  # start index of the text after string x
        end = text.index(y, start)  # end index of the text before string y
        return text[start:end].strip()  # return the text between x and y, trimming any leading/trailing white space
    except ValueError:
        return ''  # either string x or y was not found


def extract_text(my_string2):
    # The pattern looks for "MY TEXT:" or "MY TEXT2:", captures the text that follows,
    # and stops when it encounters any text ending with a colon.
    pattern = (r'(DE CE SUNT FALSE NARATIUNILE:|DE CE ESTE FALSA NARATIUNEA:|DE CE E FALSA NARATIUNEA:)(.*?)(?=\s[A-Z]+\:|$)')


    # Find all matches in the string based on the pattern
    matches = re.findall(pattern, my_string2, re.DOTALL)

    # Extract the text (group 2 in the regex pattern)
    extracted_texts = ''
    if len(matches) > 0:
        extracted_texts = ''.join([match[1].strip() for match in matches])

    return extracted_texts


# Translate data object from Romanian to English
def translate_object(data_object):
    translator = LocalTranslator()

    data_object.narrative = [translator.robust_translate(unidecode(x)) for x in data_object.narrative]
    translated_tags = []
    for x in data_object.tags:
        translated_tag = translator.robust_translate(unidecode(x))
        if translated_tag == "eu":
            translated_tag = "EU"
        translated_tag.replace(" eu ", ' EU ')
        translated_tags.append(translated_tag)
    data_object.tags = translated_tags
    if data_object.speaker_job_title != '':
        data_object.speaker_job_title = translator.robust_translate(data_object.speaker_job_title)
    if data_object.statement != '':
        data_object.statement = translator.robust_translate(data_object.statement)
    if data_object.spread_location != '':
        data_object.spread_location = translator.robust_translate(data_object.spread_location)
    if data_object.fake_news_content != '':
        data_object.fake_news_content = translator.robust_translate(data_object.fake_news_content)
    if data_object.summary_explanation != '':
        data_object.summary_explanation = translator.robust_translate(data_object.summary_explanation)
    if data_object.debunking_argument != '':
        data_object.debunking_argument = translator.robust_translate(data_object.debunking_argument)
    return data_object
