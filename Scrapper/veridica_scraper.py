import re
import requests
from bs4 import BeautifulSoup
import csv

from DataObject import DataObject
from LocalState import LocalState
from unidecode import unidecode
import json
from QueueConnectionModule import QueueConnectionModule
from LocalTranslator import Translator
from ress import extract_text, extract_text_between_strings, translate_object

localState = LocalState()
queue = QueueConnectionModule()
index = 0
total_empty = 0

'''
The main scraper iterates on the website and parses data. This will be dedicated for each wesite since we try to maximize the quality 
of the data gathered
'''


# extract the tags associated with each article and written by journalists
def extract_tags(soup):
    # This is for propaganda
    navs = soup.find_all('nav')
    extracted_tags = []
    for nav in navs:
        if "Tags:" in nav.get_text():
            # Find all <a> tags (or any other desired tags) inside the <nav>
            for a_tag in nav.find_all('a'):
                if "eticheta" in a_tag["href"]:
                    extracted_tags.append(unidecode(a_tag.get_text().strip()))
    # This is for dezinformare format
    if extracted_tags == []:
        all_tags = soup.find_all(string=re.compile("Tags:"))
        for element in all_tags:
            parent_element = element.find_parent()
            if parent_element:
                for a_tag in parent_element.find_all('a', href=True):
                    if "eticheta" in a_tag["href"]:
                        extracted_tags.append(unidecode(a_tag.get_text().strip()))
    return extracted_tags


# extract the name of the journalist
def extract_name(soup):
    image = soup.find('img', 'rounded-circle img-fluid')
    if image != None:
        return image["alt"]
    return ""

#parse the content page of the article
def parse_news_page(data_object, link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')

    cards = soup.find_all('div', 'article-content')
    summary = soup.find_all('div', 'p-3 bg-grey text-uppercase mb-3')
    data_object.tags = extract_tags(soup)
    data_object.journalist_name = extract_name(soup)

    # If I send all the HTML is too much
    # data_object.raw_page = page.content
    data_object.debunking_argument = ''.join(
        [unidecode(tag.text.strip()) for tag in cards] + [unidecode(tag.text.strip()) for
                                                          tag in summary])
    data_object.summary_explanation = extract_text(data_object.debunking_argument)
    stire_strings = extract_text_between_strings(page.content, "știre:", "narațiune:")
    data_object.fake_news_content = unidecode(stire_strings)

    naratiune_strings = soup.find_all(string=lambda text: 'narațiune cheie:' in text.lower())
    for naratiune in naratiune_strings:
        nn = soup.find(lambda tag: tag.text == naratiune in tag.text)
        parent = nn.find_parent()
        my_text = parent.text.replace("Narațiune cheie:", '').strip().lower()
        data_object.narrative.append(unidecode(my_text))

#parse the table from each page from the veridica dataset
def parse_table(table):
    global index, total_empty
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 2 and not localState.already_parsed(cols[1].find('a')['href']):
            data_object = DataObject()
            data_object.date = cols[0].text.strip()

            # here I need to remove because it's standard to add if it is either fake news or dezinformare
            statement = unidecode(cols[1].text.strip())
            statement_parts = statement.split(':')
            if not ("FAKE NEWS" in statement_parts[0]
                    or "PROPAGANDA DE RAZBOI" in statement_parts[0]
                    or "DEZINFORMARE" in statement_parts[0]):
                continue
            statement = ' '.join(statement.split(':')[1:])
            data_object.statement = statement

            # here I check if the 2nd column has a link for the source of the fake statement
            fake_news_source = cols[2].find('a')
            if fake_news_source is not None:
                data_object.fake_news_source = fake_news_source['href']
            data_object.spread_location = cols[3].text.strip()
            data_object.debunking_link = cols[1].find('a')['href']
            parse_news_page(data_object, cols[1].find('a')['href'])
            localState.append(data_object)
            translated_data_object = translate_object(data_object)
            print(json.dumps(translated_data_object.json_encoder()))
            queue.send_message(json.dumps(translated_data_object.json_encoder()))
            index = index + 1
        print(index)


        # if index > 0:
        #     exit(0)

#iterate through all the pages by navigating always to the next page
def crawl_summary_page(p):
    print(p)
    page = requests.get(p)
    soup = BeautifulSoup(page.content, 'html.parser')

    table = soup.find('table', class_="rwd-table")
    parse_table(table)

    pages = soup.find('ul', class_="pagination")
    active_page = pages.find('li', class_="active")
    next_page = active_page.find_next_sibling()
    if next_page is not None:
        next_link = next_page.find('a', class_='page-link')
        if next_link is not None and next_link['href']:
            next_link = next_link['href']
            crawl_summary_page(next_link)
    hrefs = []


#Starting at the base link the recursive crawling of each page
if __name__ == '__main__':
    pages = ['https://www.veridica.ro/baza-de-date']
    crawl_summary_page(pages[0])

