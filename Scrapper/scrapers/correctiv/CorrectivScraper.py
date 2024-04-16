import sys
import re
import spacy
import requests
from bs4 import BeautifulSoup

import DataObject
from ress import translateString, translate_object
from scrapers.BaseScraper import BaseScraper
from DataObject import DataObject

index = 0
total_empty = 0
verdict_counts = {}


class CorrectivScraper(BaseScraper):
    def __int__(self, db_filename='correctiv_local_state.csv', faulty_filename='correctiv_faulty.csv'):
        BaseScraper.__init__(self, db_filename, faulty_filename)

    def complete_info(self, data_obj: DataObject):
        if data_obj.statement is None or data_obj.statement.strip() == '':
            return False
        if data_obj.summary_explanation.strip() == '':
            return False
        if data_obj.date.strip() == '':
            return False
        if data_obj.fake_news_content.strip() == '':
            return False
        if data_obj.debunking_argument.strip() == '':
            return False
        if data_obj.verdict.strip() == '':
            return False
        if not data_obj.fake_news_source:
            return False
        if not data_obj.spread_location:
            return False
        if not data_obj.languages:
            return False
        if data_obj.debunking_link is None or data_obj.debunking_link.strip() == '':
            return False
        if not data_obj.fake_news_source or "" in data_obj.fake_news_source:
            return False
        return True

    def crawl_summary_page(self, page, rescrape_faulty=False, updates_only=False):
        global index, total_empty, verdict_counts
        print(page)
        page = requests.get(page)
        soup = BeautifulSoup(page.content, 'html.parser')

        posts = soup.find_all('a', class_='teaser__item')

        for post in posts:
            data_object = DataObject('correctiv', 'https://correctiv.org/')

            debunk_link = post['href']
            print(debunk_link)
            title = post.find('h3', class_='teaser__headline').text

            if ((not rescrape_faulty and not self.local_state.already_parsed(debunk_link)) or
                    (rescrape_faulty and self.local_state.has_faulty(debunk_link)) or
                    updates_only):
                if updates_only and (
                        self.local_state.has_faulty(debunk_link) or self.local_state.already_parsed(debunk_link)):
                    print("Finish updates")
                    exit(0)
                if rescrape_faulty and self.manual_inputted_data(debunk_link, rescrape_faulty):
                    continue

                short_description = post.find('p', class_='teaser__lead').get_text(strip=True)

                data_object.debunking_link = debunk_link
                data_object.summary_explanation = short_description
                data_object.spread_location = ['Germany']
                data_object.languages = ['German']
                self.scrapeRestData(data_object)

                data_object = translate_object(data_object)
                if self.complete_info(data_object):
                    self.send_data(data_object, rescrape_faulty)
                else:
                    self.local_state.append_faulty(data_object)

            index += 1
            print(index)
        for verdict, count in verdict_counts.items():
            print(f'"{verdict}" apare de {count} ori.')

    def scrapeRestData(self, data_object):
        page = requests.get(data_object.debunking_link)
        soup = BeautifulSoup(page.content, 'html.parser')

        self.getClaimAndVerdict(soup, data_object)
        if data_object.statement == '':
            return
        self.getContent(soup, data_object)

    def getClaimAndVerdict(self, soup, data_object):
        global verdict_counts
        detail_boxes = soup.find_all('div', class_='detail__box')

        # Iterăm prin fiecare detail_box pentru a verifica titlul și a extrage conținutul corespunzător
        for box in detail_boxes:
            title = box.find('div', class_='detail__box-title').text.strip()
            if title == "Behauptung":  # aici e claim
                content = box.find('div', class_='detail__box-content')
                claim = content.text.strip() if content else ""
                divs = box.find('div', class_='detail__box-footer').find_all('div')

                # Extragem textul din al doilea div și înlăturăm "Datum: " și orice spații albe excesive
                dateText = ''
                spreadSource = []
                if len(divs) > 1:  # Asigură-te că există cel puțin două div-uri
                    spreadSource = self.getFakeNewsSource(divs[0].text.strip().replace("Aufgestellt von: ", "").strip())
                    dateText = divs[1].text.replace("Datum:", "").strip()
                data_object.statement = claim
                data_object.fake_news_source = spreadSource
                data_object.date = dateText

            if title == 'Bewertung':  # aici e verdict
                verdict = box.find('div', class_='detail__rating-text').find('strong').text.strip()
                if verdict == 'Richtig' or verdict == 'Größtenteils richtig':
                    verdict = ''
                verdict = translateString(verdict)
                fakeNewsContent = box.find('div', class_='detail__rating').next_sibling.strip()
                data_object.verdict = verdict
                data_object.fake_news_content = fakeNewsContent

    def getContent(self, soup, data_object):
        content = soup.find('div', class_='detail__content')
        content = content.text.split('Redigatur')[0].strip()
        data_object.debunking_argument = content

    def getFakeNewsSource(self, source):
        source = self.clean_string(source)
        sources = self.spliSource(source)
        for i, s in enumerate(sources):
            if s == 'Xund Tiktok':
                sources[i] = 'X'
                sources.append('Tiktok')
            if s == 'Tiktokund Twitter':
                sources[i] = 'Twitter'
                sources.append('Tiktok')
            if s == 'Facebookund Tiktok' or s == 'TikTokund Facebook':
                sources[i] = 'Facebook'
                sources.append('Tiktok')
            if s == 'Facebookund Whatsapp':
                sources[i] = 'Facebook'
                sources.append('Whatsapp')
            if s == 'Telegramund Twitter' or s == 'Twitterund Telegram':
                sources[i] = 'Telegram'
                sources.append('Twitter')
            if s == 'Facebookund Twitter' or s == 'Twitterund Facebook' or s == 'Twitter-und Facebook':
                sources[i] = 'Facebook'
                sources.append('Twitter')
            if s == 'Facebookund Telegram' or s == 'Telegramund Facebook' or s == 'Telegram-; Facebook' or s == 'Facebookund Telegram-':
                sources[i] = 'Facebook'
                sources.append('Telegram')
            elif s == 'und Facebook' or s == 'Diverse Facebook' or s == 'Facebook-Post' or s == 'Facebook-' or s == 'Faceook':
                sources[i] = 'Facebook'
            elif s == 'Tiktok-':
                sources[i] = 'Tiktok'
            elif s == 'Twitter-':
                sources[i] = 'Twitter'
            elif s == 'Telegram-' or s == 'Telegram-Nutzer':
                sources[i] = 'Telegram'
            elif s == 'Youtube-':
                sources[i] = 'Youtube'
            elif s == 'X ()' or s == 'X()':
                sources[i] = 'X'
        sources = [s for s in sources if s.strip() != '']
        sources = [translateString(s) for s in sources]
        return sources

    def clean_string(self, input_string):
        patterns = [
            r'Beitrag',
            r'Beiträge in',
            r'Beiträgen in',
            r'Beiträgen auf',
            r'Beitrag bei',
            r'Viraler',
            r'virale',
            r'viralen',
            r'virales',
            r'-Beiträgen',
            r'-Beiträge',
            r'Beträgen auf',
            r'Anzeigen auf',
            r'-Video',
            r'-Videos',
            r'Videos auf',
            r'auf',
            r'bei',
            r'in',
            r'\(',
            r'\)',
            r'ehemals Twitter',
        ]

        combined_pattern = r'\b(' + '|'.join(pattern.strip('-') for pattern in patterns) + r')\b'
        cleaned_string = re.sub(combined_pattern, '', input_string, flags=re.IGNORECASE)
        cleaned_string = re.sub(r'-\s|-$', '', cleaned_string.strip())
        cleaned_string = re.sub(r'\s+', ' ', cleaned_string).strip()

        return cleaned_string

    def spliSource(self, source):
        uniform_string = re.sub(r'\s+und\s+', ',', source)
        if ',' in uniform_string:

            return [element.strip() for element in uniform_string.split(',') if element.strip()]
        # Dacă nu sunt găsite delimitatoare, returnăm un array cu string-ul original ca element unic
        else:
            return [source.strip()]

if __name__ == '__main__':
    """
    Starting at the base link the recursive crawling of each page
    The argumens can be: 
        scarpe_all: which scrapes all the data, 
        rescrape_faulty: which rescrapes only the elements which are in the faulty list. 
            This is for improvements in code for the elements with missing fields. 
            If in the faulty files it is added manual_verification TRUE then it just sends manually completed data 
            from the file dirrectly to the aggregator
        updates_only: here the code scrapes the wesite and stops at the first element encountered before since it consideres
            that from there on all the data is scraped         
    """
    correctivScraper = CorrectivScraper(db_filename='correctiv_local_state.csv',
                                        faulty_filename='correctiv_faulty.csv')

    pages = ['https://correctiv.org/faktencheck/naher-osten/', 'https://correctiv.org/faktencheck/russland-ukraine/',
             'https://correctiv.org/faktencheck/energiekrise-strompreise-gas/',
             'https://correctiv.org/faktencheck/coronavirus/', 'https://correctiv.org/faktencheck/klima/',
             'https://correctiv.org/faktencheck/migration/',
             'https://correctiv.org/faktencheck/medizin-und-gesundheit/', 'https://correctiv.org/faktencheck/politik/',
             'https://correctiv.org/faktencheck/affenpocken/']

    if len(sys.argv) < 2:
        print("run this program with arguments: scrape_all, rescrape_faulty, updates_only")
    if sys.argv[1] == "scrape_all":
        for page in pages:
            correctivScraper.crawl_summary_page(page)
    elif sys.argv[1] == "rescrape_faulty":
        for page in pages:
            correctivScraper.crawl_summary_page(page, rescrape_faulty=True)
    elif sys.argv[1] == "updates_only":
        for page in pages:
            correctivScraper.crawl_summary_page(page, rescrape_faulty=False, updates_only=True)
