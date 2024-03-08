import re
import requests
from bs4 import BeautifulSoup
from DataObject import DataObject
from LocalState import LocalState
from unidecode import unidecode
import json
from QueueConnectionModule import QueueConnectionModule
from ress import extract_text, extract_text_between_strings, translate_object
import sys

from scrapers.BaseScraper import BaseScraper

index = 0
total_empty = 0

'''
The main scraper iterates on the website and parses data. This will be dedicated for each wesite since we try to maximize the quality 
of the data gathered
'''


class VeridicaScraper(BaseScraper):
    def __int__(self, db_filename='veridica_local_state.csv', faulty_filename='veridica_faulty.csv'):
        BaseScraper.__init__(self, db_filename, faulty_filename)

    def extract_tags(self, soup):
        '''
        extract the tags associated with each article and written by journalists
        '''
        navs = soup.find_all('nav')
        extracted_tags = []
        for nav in navs:
            if "Tags:" in nav.get_text():
                # Find all <a> tags (or any other desired tags) inside the <nav>
                for a_tag in nav.find_all('a'):
                    extracted_tags.append(unidecode(a_tag.get_text().strip()))
        # This is for dezinformare format
        if extracted_tags == []:
            all_tags = soup.find_all(string=re.compile("Tags:"))
            for element in all_tags:
                parent_element = element.find_parent()
                if parent_element:
                    for a_tag in parent_element.find_all('a', href=True):
                        if "https://www.veridica.ro/en/articles/tag/" in a_tag['href']:
                            extracted_tags.append(unidecode(a_tag.get_text().strip()))
        return extracted_tags

    def extract_media_outlets(self, soup):
        uls = soup.find_all('li')
        extracted_channels = []
        for ul in uls:
            if "Amplification:" in ul.get_text():
                # Find all <a> tags (or any other desired tags) inside the <nav>
                text = ul.get_text()
                text = text.replace("Amplification:", '')
                channels = [t.strip() for t in text.split(',') if t.strip() != 'ETC.']
                extracted_channels.extend(channels)

        return extracted_channels

    def extract_name(self, soup):
        """
        # extract the name of the journalist
        """
        image = soup.find('img', 'rounded-circle img-fluid')
        if image != None:
            return image["alt"]
        return ""

    def parse_news_page(self, data_object, link):
        """
        parse the content page of the article
        """
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')

        cards = soup.find_all('div', 'article-content')
        summary = soup.find_all('div', 'p-3 bg-grey text-uppercase mb-3')
        data_object.tags = self.extract_tags(soup)
        data_object.fake_news_source.extend(self.extract_media_outlets(soup))
        data_object.journalist_name = self.extract_name(soup)

        # If I send all the HTML is too much
        # data_object.raw_page = page.content
        data_object.debunking_argument = ''.join(
            [unidecode(tag.text.strip()) for tag in cards] + [unidecode(tag.text.strip()) for
                                                              tag in summary])
        data_object.summary_explanation = extract_text(data_object.debunking_argument)

        stire_strings = extract_text_between_strings(page.content, "news:", "narrative:")
        data_object.fake_news_content = unidecode(stire_strings)

        naratiune_strings = soup.find_all(string=lambda text: 'key narrative:' in text.lower())
        for naratiune in naratiune_strings:
            nn = soup.find(lambda tag: tag.text == naratiune in tag.text)
            parent = nn.find_parent()
            my_text = parent.text.replace("key narrative:", '').strip().lower()
            data_object.narrative.append(unidecode(my_text))

    def complete_info(self, data_obj):
        """
        Check if the object is complete and ready to be sent.
        This validation is done in order to reduce faulty data inserted in the system
        """
        if data_obj.statement is None or data_obj.statement.strip() == '':
            return False
        if data_obj.fake_news_source == []:
            return False
        if data_obj.narrative == []:
            return False
        if data_obj.spread_location == []:
            return False
        if data_obj.debunking_link is None or data_obj.debunking_link.strip() == '':
            return False
        return True


    def get_main_table_info(self, cols):
        """
        The main info from the table is extracted: date, statement, source, link and spread location
        :param cols: main table columns
        :return: None (no fakenews, disinfo or war propaganda found and that means that the element is not valid)
                or data_object contianing scraped information
        """
        data_object = DataObject()
        data_object.date = cols[0].text.strip()
        # here I need to remove because it's standard to add if it is either fake news or disinfo
        statement = unidecode(cols[1].text.strip())
        statement_parts = statement.split(':')
        if not ("FAKE NEWS" in statement_parts[0]
                or "WAR PROPAGANDA" in statement_parts[0]
                or "DISINFORMATION" in statement_parts[0]):
            return None
        statement = ' '.join(statement.split(':')[1:])
        data_object.statement = statement

        # here I check if the 2nd column has a link for the source of the fake statement
        fake_news_source = cols[2].find('a')
        if fake_news_source is not None:
            data_object.fake_news_source = [fake_news_source['href']]
        if cols[3].text.strip() is not None or cols[3].text.strip() != '':
            data_object.spread_location = [cols[3].text.strip()]
        else:
            data_object.spread_location = 'Romania'
        data_object.debunking_link = cols[1].find('a')['href']
        return data_object


    def manual_inputted_data(self, debunking_link, rescrape_faulty):
        """
        If manual inputed data is found, then it just reads from the faulty csv and sends it directly to the aggregator
        :param debunking_link rescrape_faulty:
        :return: True (manual data is found), False (no manual data was found)
        """
        element = self.local_state.manual_verification(debunking_link)
        if element is not None:
            self.send_data(element, rescrape_faulty)
            return True
        return False


    def parse_table(self, table, rescrape_faulty=False, updates_only=False):
        """
        Parse the table from each page from the Veridica dataset
        :param table: main table from the website with general information about the data
        At first tests in which case the code is in: scrape_all, rescrape_faulty or updates_only
            if the code is in rescrape faulty, check if manual data was inserted
            if manual data was inserted it can move to next because there is no need to scrape
        Get the information from the main table
            if the infor is not disinfor or fakenews -> data object is none and then it continues with the next element
         parse the news page for additional information. Get into details
         translate the object in english
         if the data is complete send it and add in local state, if not then consider it faulty and do not send
        """
        global index, total_empty
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if (len(cols) >= 2 and (
                    (not rescrape_faulty and not self.local_state.already_parsed(cols[1].find('a')['href'])) or
                    (rescrape_faulty and self.local_state.has_faulty(cols[1].find('a')['href'])) or
                    (updates_only)
            )):

                debunking_link = cols[1].find('a')['href']
                if updates_only and (self.local_state.has_faulty(debunking_link) or self.local_state.already_parsed(debunking_link)):
                    print("Finish updates")
                    exit(0)
                if rescrape_faulty and self.manual_inputted_data(debunking_link, rescrape_faulty):
                    continue
                data_object = self.get_main_table_info(cols)
                if data_object is None:
                    continue

                self.parse_news_page(data_object, cols[1].find('a')['href'])
                data_object = translate_object(data_object)
                if self.complete_info(data_object):
                    self.send_data(data_object, rescrape_faulty)
                else:
                    self.local_state.append_faulty(data_object)
                index = index + 1
            print(index)
            # if index > 0:
            #     exit(0)


    def crawl_summary_page(self, p, rescrape_faulty=False, updates_only=False):
        """
        iterate through all the pages by navigating always to the next page
        :param p: main page
        :param rescrape_faulty:  if rescraping only faulty messages
        :param updates_only: if searching only for updates
        """
        print(p)
        page = requests.get(p)
        soup = BeautifulSoup(page.content, 'html.parser')

        table = soup.find('table', class_="rwd-table")
        self.parse_table(table, rescrape_faulty, updates_only)

        pages = soup.find('ul', class_="pagination")
        active_page = pages.find('li', class_="active")
        next_page = active_page.find_next_sibling()
        if next_page is not None:
            next_link = next_page.find('a', class_='page-link')
            if next_link is not None and next_link['href']:
                next_link = next_link['href']
                self.crawl_summary_page(next_link, rescrape_faulty, updates_only)
        hrefs = []


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
    veridica_scraper = VeridicaScraper(db_filename='veridica_local_state.csv', faulty_filename='veridica_faulty.csv')
    if len(sys.argv) < 2:
        print("run this program with arguments: scrape_all, rescrape_faulty, updates_only")
    if sys.argv[1] == "scrape_all":
        pages = ['https://www.veridica.ro/en/database']
        veridica_scraper.crawl_summary_page(pages[0])
    elif sys.argv[1] == "rescrape_faulty":
        pages = ['https://www.veridica.ro/en/database']
        veridica_scraper.crawl_summary_page(pages[0], rescrape_faulty=True)
    elif sys.argv[1] == "updates_only":
        pages = ['https://www.veridica.ro/en/database']
        veridica_scraper.crawl_summary_page(pages[0], rescrape_faulty=False, updates_only=True)
