import re
import requests
from bs4 import BeautifulSoup
import csv

from DataObject import DataObject
from LocalState import LocalState
from unidecode import unidecode
import json
from QueueConnectionModule import QueueConnectionModule

localState = LocalState()
queue = QueueConnectionModule()


def extract_text_between_strings(html, x, y):
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text().lower()  # get all text, discarding tags
    try:
        start = text.index(x) + len(x)  # start index of the text after string x
        end = text.index(y, start)  # end index of the text before string y
        return text[start:end].strip()  # return the text between x and y, trimming any leading/trailing white space
    except ValueError:
        return ''  # either string x or y was not found

def parse_news_page(data_object, link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')

    cards = soup.find_all('div', 'article-content')
    summary = soup.find_all('div', 'p-3 bg-grey text-uppercase mb-3')

    #If I send all the HTML is too much
    #data_object.raw_page = page.content
    data_object.debunking_argument = [unidecode(tag.text.strip()) for tag in cards] + [unidecode(tag.text.strip()) for tag in summary]
    stire_strings = extract_text_between_strings(page.content, "știre:", "narațiune:")
    data_object.fake_news_content = stire_strings

    '''naratiune_strings = soup.find_all(string=lambda text: 'narațiune' in text.lower())
    for naratiune in naratiune_strings:

        if naratiune.text.lower() == "narațiune:":
            nn = soup.find(lambda tag: tag.text == naratiune in tag.text)
            next_paragraph = nn.find_next_sibling()
            if next_paragraph is not None:
                data_object.narrative.append(unidecode(naratiune.text.strip()) + ' ' + unidecode(next_paragraph.text.strip()))
        else:
            data_object.narrative.append(unidecode(naratiune.text.strip()))
    '''
    naratiune_strings = soup.find_all(string=lambda text: 'narațiune cheie:' in text.lower())
    for naratiune in naratiune_strings:
        nn = soup.find(lambda tag: tag.text == naratiune in tag.text)
        parent = nn.find_parent()
        my_text = parent.text.replace("Narațiune cheie:", '').strip().lower()
        data_object.narrative.append(unidecode(my_text))

def parse_table(table):
    rows = table.find_all('tr')
    i = 0
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 2 and not localState.already_parsed(cols[1].find('a')['href']):
            data_object = DataObject()
            data_object.date = cols[0].text.strip()

            #here I need to remove because it's standard to add if it is either fake news or dezinformare
            statement = unidecode(cols[1].text.strip())
            statement = ' '.join(statement.split(':')[1:])
            data_object.statement = statement

            # here I check if the 2nd column has a link for the source of the fake statement
            fake_news_source = cols[2].find('a')
            if fake_news_source is not None:
                data_object.fake_news_source = fake_news_source['href']
            data_object.spread_country = cols[3].text.strip()
            data_object.debunking_link = cols[1].find('a')['href']
            print(cols[1].find('a')['href'])
            parse_news_page(data_object, cols[1].find('a')['href'])
            localState.append(data_object)
            queue.send_message(json.dumps(data_object.json_encoder()))
            i = i + 1
        print(i)
        #if i > 0:
        #    exit(0)


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


if __name__ == '__main__':
    pages = ['https://www.veridica.ro/baza-de-date']
    crawl_summary_page(pages[0])

