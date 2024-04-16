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


class Infoveritas(BaseScraper):
    def __int__(self, db_filename='infoveritas_local_state.csv', faulty_filename='infoveritas_faulty.csv'):
        BaseScraper.__init__(self, db_filename, faulty_filename)

    def complete_info(self, data_obj: DataObject):
        if data_obj.statement is None or data_obj.statement.strip() == '':
            return False
        if data_obj.date.strip() == '':
            return False
        if data_obj.debunking_argument.strip() == '':
            return False
        if not data_obj.spread_location:
            return False
        if not data_obj.languages:
            return False
        if data_obj.debunking_link is None or data_obj.debunking_link.strip() == '':
            return False
        if not data_obj.tags or "" in data_obj.tags:
            return False
        if not data_obj.fake_news_source or "" in data_obj.fake_news_source:
            return False
        return True

    def crawl_summary_page(self, page, rescrape_faulty=False, updates_only=False):
        global index, total_empty
        page = requests.get(page)
        soup = BeautifulSoup(page.content, 'html.parser')

        posts = soup.find_all('article', class_='l-post grid-post grid-base-post')

        for post in posts:
            data_object = DataObject('infoveritas', 'https://info-veritas.com/')
            debunk_link = post.find('a', class_='image-link')['href']
            print(debunk_link)

            if ((not rescrape_faulty and not self.local_state.already_parsed(debunk_link)) or
                    (rescrape_faulty and self.local_state.has_faulty(debunk_link)) or
                    updates_only):
                if updates_only and (
                        self.local_state.has_faulty(debunk_link) or self.local_state.already_parsed(debunk_link)):
                    print("Finish updates")
                    exit(0)
                if rescrape_faulty and self.manual_inputted_data(debunk_link, rescrape_faulty):
                    continue

                data_object.debunking_link = debunk_link
                data_object.spread_location = ['Spain']
                data_object.languages = ['Spanish']
                self.scrapeDataFromLink(data_object)

                data_object = translate_object(data_object)
                self.getSpreadSource(data_object)
                if self.complete_info(data_object):
                    self.send_data(data_object, rescrape_faulty)
                else:
                    self.local_state.append_faulty(data_object)

            index += 1
            print(index)

        next_page_link_element = soup.find('a', class_='next page-numbers')

        if next_page_link_element:
            next_page_link = next_page_link_element['href']
            self.crawl_summary_page(next_page_link, rescrape_faulty, updates_only)

    def scrapeDataFromLink(self, data_object):
        page = requests.get(data_object.debunking_link)
        soup = BeautifulSoup(page.content, 'html.parser')

        title = soup.find('h1', class_='is-title post-title').text.strip()
        data_object.statement = title
        debunkArgument = soup.find('div', class_='post-content').text.strip()
        pos = debunkArgument.find('Fuentes')

        if pos != -1:
            debunkArgument = debunkArgument[:pos]
        data_object.debunking_argument = debunkArgument

        data_object.date = self.getDateFromString(soup.find('time', class_='post-date')['datetime'])
        summaryExpl = soup.find('div', class_='sub-title')
        if summaryExpl:
            data_object.summary_explanation = summaryExpl.text.strip()
        self.getTags(soup, data_object)


    def getDateFromString(self, date):
        date_obj = datetime.fromisoformat(date)
        formatted_date = date_obj.strftime("%d.%m.%Y")
        return formatted_date

    def getTags(self, soup, data_object):
        tags_elements = soup.find('div', class_='the-post-tags')
        if tags_elements:
            tags_elements = tags_elements.find_all('a')
            tags = [tag.get_text(strip=True) for tag in tags_elements]
            data_object.tags = tags

    def getSpreadSource(self, data_object):
        identifier = FakeNewsChannelIdentifier()
        fake_news_channel, debunk_channel = identifier.identify_channels(data_object.debunking_argument)
        for chanel in debunk_channel:
            if chanel == 'example website':
                print("Am avut example")
                return
        if 'Infoveritas' in debunk_channel:
            debunk_channel.remove('Infoveritas')
        if 'Infoveritas' in fake_news_channel:
            fake_news_channel.remove('Infoveritas')

        print("Channels that disseminated the fake news:", fake_news_channel)
        print("Channels that contributed to the debunking:", debunk_channel)
        data_object.fake_news_source = fake_news_channel
        data_object.debunk_sources = debunk_channel


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
    infoveritasScraper = Infoveritas(db_filename='infoveritas_local_state.csv',
                                        faulty_filename='infoveritas_faulty.csv')

    pages = ['https://info-veritas.com/category/desinformacion/']

    if len(sys.argv) < 2:
        print("run this program with arguments: scrape_all, rescrape_faulty, updates_only")
    if sys.argv[1] == "scrape_all":
        for page in pages:
            infoveritasScraper.crawl_summary_page(page)
    elif sys.argv[1] == "rescrape_faulty":
        for page in pages:
            infoveritasScraper.crawl_summary_page(page, rescrape_faulty=True)
    elif sys.argv[1] == "updates_only":
        for page in pages:
            infoveritasScraper.crawl_summary_page(page, rescrape_faulty=False, updates_only=True)
