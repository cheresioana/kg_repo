import locale
import sys
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

import DataObject
from ress import translateString, translate_object
from scrapers.BaseScraper import BaseScraper
from DataObject import DataObject

index = 0
total_empty = 0
verdict_counts = {}


class DemagogScraper(BaseScraper):
    def __int__(self, db_filename='demagogcz_local_state.csv', faulty_filename='demagogcz_faulty.csv'):
        BaseScraper.__init__(self, db_filename, faulty_filename)

    def complete_info(self, data_obj: DataObject):
        if data_obj.statement is None or data_obj.statement.strip() == '':
            return False
        if data_obj.date.strip() == '':
            return False
        if data_obj.verdict.strip() == '':
            return False
        if data_obj.debunking_argument.strip() == '':
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
        global index, total_empty
        print(page)
        page = requests.get(page)
        soup = BeautifulSoup(page.content, 'html.parser')

        posts = soup.find_all('article', class_='s-statement')

        for post in posts:
            data_object = DataObject('demagogCZ', 'https://demagog.cz/')

            acordion = post.find('div', class_='accordion')
            if acordion:
                thirdDiv = acordion.find('div', class_='justify-content-between')
                linkElement = thirdDiv.find('a', class_='align-items-center')
            else:
                linkElement = post.find('div', class_='d-flex justify-content-end align-items-center w-100').find('a')
            if linkElement:
                debunk_link = 'https://demagog.cz' + linkElement['href']
            else:
                self.local_state.append_faulty(data_object)
                index += 1
                continue
            verdictDiv = post.find('div', class_='col-lg-5')
            verdictDiv = verdictDiv.find('div', class_='d-flex align-items-center mb-2')
            verdictSpan = verdictDiv.find('span', class_='fs-600')

            verdict = ''
            if verdictSpan:
                verdict = verdictSpan.text.strip()
            if verdict == 'Pravda' or verdict == '':
                print(verdict)
                data_object.debunking_link = debunk_link
                data_object.verdict = verdict
                self.local_state.append_faulty(data_object)
                index += 1
                continue

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
                print(data_object.debunking_link)
                data_object.verdict = translateString(verdict)
                data_object.spread_location = ['Czechia']
                data_object.languages = ['Czech']
                self.scrapeRestData(data_object)

                data_object = translate_object(data_object)
                if self.complete_info(data_object):
                    self.send_data(data_object, rescrape_faulty)
                else:
                    self.local_state.append_faulty(data_object)

            index += 1
            print(index)

        next_page_link_element = soup.find('nav', class_='pagination')
        if next_page_link_element:
            next_page_link_element = next_page_link_element.find('span', class_='next')
        if next_page_link_element:
            next_page_link = 'https://demagog.cz/' + next_page_link_element.find('a')['href']
            self.crawl_summary_page(next_page_link, rescrape_faulty, updates_only)

    def scrapeRestData(self, data_object):
        page = requests.get(data_object.debunking_link)
        soup = BeautifulSoup(page.content, 'html.parser')

        statement = soup.find('blockquote').find('span', class_='fs-6').text.strip()
        data_object.statement = statement
        date = soup.find('span', class_='date').text
        self.getSpreadSourceName(data_object, soup)
        self.getDateFromCzech(data_object, date)
        self.getExplain(data_object, soup)

    def getDateFromCzech(self, data_object, date):
        old_locale = locale.getlocale(locale.LC_TIME)
        locale.setlocale(locale.LC_TIME, 'cs_CZ.UTF-8')
        date_datetime = datetime.strptime(date, '%d. %B %Y')
        locale.setlocale(locale.LC_TIME, old_locale)
        data_object.date = date_datetime.strftime('%d.%m.%Y')

    def getExplain(self, data_object, soup):
        divs = soup.find_all('div', class_='mb-10')
        for div in divs:
            h3 = div.find('h3')
            if h3:
                text = h3.text.strip()
                if text == 'Zkrácené odůvodnění':
                    summaryExpl = div.find('p', class_='fs-5').text.strip()
                    data_object.summary_explanation = summaryExpl
                elif text == 'Plné odůvodnění':
                    debunking_argument = div.find('div', class_='content').text.strip()
                    data_object.debunking_argument = debunking_argument

    def getSpreadSourceName(self, data_object, soup):
        spreadSource = []
        div = soup.find('div', class_='col-4')
        h3 = div.find('h3', class_='fs-6 fs-bold').text.strip()
        spreadSource = [h3]
        data_object.fake_news_source = spreadSource


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
    DemagogScraper = DemagogScraper(db_filename='demogogCZ_local_state.csv',
                                        faulty_filename='demogogCZ_faulty.csv')

    pages = ['https://demagog.cz/vyroky']

    if len(sys.argv) < 2:
        print("run this program with arguments: scrape_all, rescrape_faulty, updates_only")
    if sys.argv[1] == "scrape_all":
        for page in pages:
            DemagogScraper.crawl_summary_page(page)
    elif sys.argv[1] == "rescrape_faulty":
        for page in pages:
            DemagogScraper.crawl_summary_page(page, rescrape_faulty=True)
    elif sys.argv[1] == "updates_only":
        for page in pages:
            DemagogScraper.crawl_summary_page(page, rescrape_faulty=False, updates_only=True)