import sys
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

import DataObject
from openAI import FakeNewsChannelIdentifier
from ress import translateString, translate_object
from scrapers.BaseScraper import BaseScraper
from DataObject import DataObject

index = 0
total_empty = 0
verdict_counts = {}


class PoligrafoScraper(BaseScraper):
    def __int__(self, db_filename='infoveritas_local_state.csv', faulty_filename='infoveritas_faulty.csv'):
        BaseScraper.__init__(self, db_filename, faulty_filename)

    def complete_info(self, data_obj: DataObject):
        if data_obj.statement is None or data_obj.statement.strip() == '':
            return False
        if data_obj.date.strip() == '':
            return False
        if data_obj.verdict.strip() == '':
            return False
        if data_obj.fake_news_content.strip() == '':
            return False
        if data_obj.debunking_argument.strip() == '':
            return False
        if not data_obj.spread_location:
            return False
        if not data_obj.languages:
            return False
        if data_obj.debunking_link is None or data_obj.debunking_link.strip() == '':
            return False
        return True

    def crawl_summary_page(self, page, rescrape_faulty=False, updates_only=False):
        global index, total_empty
        print(page)
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        })

        response = session.get(page)

        soup = BeautifulSoup(response.content, 'html.parser')
        print(soup)
        exit()
        posts = soup.find_all('article', class_='fact-check')


        for post in posts:
            data_object = DataObject('poligrafo', 'https://poligrafo.sapo.pt/')

            debunk_link = 'https://poligrafo.sapo.pt' + post.find('h3', class_='title').find('a')['href']

            if ((not rescrape_faulty and not self.local_state.already_parsed(debunk_link)) or
                    (rescrape_faulty and self.local_state.has_faulty(debunk_link)) or
                    updates_only):
                if updates_only and (
                        self.local_state.has_faulty(debunk_link) or self.local_state.already_parsed(debunk_link)):
                    print("Finish updates")
                    exit(0)
                if rescrape_faulty and self.manual_inputted_data(debunk_link, rescrape_faulty):
                    continue

                title = post.find('h3', class_='title').find('a').text.strip()
                fakenewsContent = post.find('div', class_='excerpt').text.strip()

                data_object.debunking_link = debunk_link
                data_object.statement = title
                data_object.fake_news_content = fakenewsContent
                data_object.spread_location = ['Portugal']
                data_object.languages = ['Portuguese']
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

        next_page_link_element = soup.find('li', class_='next')

        if next_page_link_element and 'disabled' not in next_page_link_element.get('class', []):
            next_page_link = 'https://poligrafo.sapo.pt/fact-checks' + next_page_link_element.find('a')['href']
            self.crawl_summary_page(next_page_link, rescrape_faulty, updates_only)

    def scrapeRestData(self, data_object):
        page = requests.get(data_object.debunking_link)
        soup = BeautifulSoup(page.content, 'html.parser')

        verdict_element = soup.find('div', class_='final-fact-check-evaluation')
        verdict = ''
        if verdict_element:
            verdict = verdict_element.text.strip()
            if verdict == 'Verdadeiro, mas...' or verdict == 'Verdadeiro':
                verdict = ''
        data_object.verdict = verdict

        if verdict in verdict_counts:
            verdict_counts[verdict] += 1
        else:
            verdict_counts[verdict] = 1

        date = self.getDateFromPortughese(soup, data_object)
        data_object.date = date
        content = soup.find('div', class_='content').text.strip()
        data_object.debunking_argument = content
        self.getSpreadSource(data_object)

    def getDateFromPortughese(self, soup, data_object):
        month_map = {
            "jan": 1,
            "fev": 2,
            "mar": 3,
            "abr": 4,
            "mai": 5,
            "jun": 6,
            "jul": 7,
            "ago": 8,
            "set": 9,
            "out": 10,
            "nov": 11,
            "dez": 12,
        }
        date = soup.find('div', class_='date')
        day = date.find('span', class_='day').text.strip()
        month = date.find('span', class_='month').text.strip()
        year = date.find('span', class_='year').text.strip()

        # Convertirea lunii din portugheză în număr
        month_number = month_map[month.lower()]
        date_obj = datetime(year=int(year), month=month_number, day=int(day))
        formatted_date = date_obj.strftime("%d.%m.%Y")

        return formatted_date

    def getSpreadSource(self, data_object):
        identifier = FakeNewsChannelIdentifier()
        fake_news_channel, debunk_channel = identifier.identify_channels("test")
        data_object.fake_news_source = fake_news_channel
        data_object.debunking_link = debunk_channel


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
    poligrafoScraper = PoligrafoScraper(db_filename='poligrafo_local_state.csv',
                                        faulty_filename='poligrafo_faulty.csv')

    pages = ['https://poligrafo.sapo.pt/fact-checks/sociedade/',
             'https://poligrafo.sapo.pt/fact-checks/politica/',
             'https://poligrafo.sapo.pt/fact-checks/internacional/',
             'https://poligrafo.sapo.pt/fact-checks/economia/',
             'https://poligrafo.sapo.pt/fact-checks/facebook/',
             'https://poligrafo.sapo.pt/fact-checks/desporto/',
             'https://poligrafo.sapo.pt/fact-checks/legislativas-2019/',
             'https://poligrafo.sapo.pt/fact-checks/legislativas2022/']

    if len(sys.argv) < 2:
        print("run this program with arguments: scrape_all, rescrape_faulty, updates_only")
    if sys.argv[1] == "scrape_all":
        for page in pages:
            poligrafoScraper.crawl_summary_page(page)
    elif sys.argv[1] == "rescrape_faulty":
        for page in pages:
            poligrafoScraper.crawl_summary_page(page, rescrape_faulty=True)
    elif sys.argv[1] == "updates_only":
        for page in pages:
            poligrafoScraper.crawl_summary_page(page, rescrape_faulty=False, updates_only=True)