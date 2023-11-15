from DataObject import DataObject
from LocalTranslator import LocalTranslator
from googletrans import Translator
import unittest

from veridica_scraper import parse_news_page
from ress import extract_text

'''
Unit tests for the scraper
'''
class TestBasicFunctions(unittest.TestCase):

    def test_translator(self):
        text = "Ioana are mere"
        translator = LocalTranslator()
        result = translator.robust_translate(text)
        self.assertEqual(result, 'Ioana has apples')

    def test_extract_narative(self):
        text = '''
        DE CE SUNT FALSE NARATIUNILE:  Republica Moldova si Romania discuta de mai multi ani despre necesitatea constructiei de noi poduri peste
        '''
        extracted_text = extract_text(text)
        expected_result = 'Republica Moldova si Romania discuta de mai multi ani despre necesitatea constructiei de noi poduri peste'
        self.assertEqual(expected_result, extracted_text)

    def test_extract_narative2(self):
        text = '''DE CE SUNT FALSE NARATIUNILE: Helo Ioana'''
        extracted_text = extract_text(text)
        expected_result = 'Helo Ioana'
        self.assertEqual(expected_result, extracted_text)

    def test_parse(self):
        data = DataObject()
        page = 'https://www.veridica.ro/stiri-false/propaganda-de-razboi-razboiul-a-salvat-rusia-de-somaj-si-saracie'
        parse_news_page(data, page)
        self.assertEqual(['Rusia' , 'Vladimir Putin' , 'Razboi in Ucraina' , 'propaganda de razboi'], data.tags)
        self.assertEqual("Marin Gherman", data.journalist_name)

    def test_parse2(self):
        data = DataObject()
        page = 'https://www.veridica.ro/stiri-false/fake-news-soros-vrea-sa-asedieze-rusia-capturand-fostele-state-sovietice-moldova-si-armenia-primii-sai-pioni'
        parse_news_page(data, page)
        self.assertEqual(['Republica Moldova', 'Ucraina', 'Rusia'], data.tags)
        self.assertEqual("Marianna Prysiazhniuk", data.journalist_name)

    def test_parse3(self):
        data = DataObject()
        page = 'https://www.veridica.ro/dezinformare/dezinformare-sanctiunile-au-consolidat-economia-rusiei-iar-ue-sprijina-rusofobia-din-ucraina-si-statele-baltice'
        parse_news_page(data, page)
        self.assertEqual(['Ucraina', 'Rusia', 'UE'], data.tags)
        self.assertEqual("Marin Gherman", data.journalist_name)

    def test_parse_euvsDisinfo1(self):
        data = DataObject()
        page = 'https://euvsdisinfo.eu/report/events-in-israel-and-ukraine-are-no-accident-as-the-us-tried-to-create-areas-of-instability'
        parse_news_page(data, page)
        self.assertEqual(['Ucraina', 'Rusia', 'UE'], data.tags)
        self.assertEqual("Marin Gherman", data.journalist_name)


if __name__ == '__main__':
    unittest.main()


