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
# queue = QueueConnectionModule()
index = 0
total_empty = 0

'''
The main scraper iterates on the website and parses data. This will be dedicated for each wesite since we try to maximize the quality 
of the data gathered
'''


# extract the name of the journalist
def extract_name(soup):
    image = soup.find('img', 'rounded-circle img-fluid')
    if image != None:
        return image["alt"]
    return ""


def try_find_verdict_in_new_page(title_link):
    page = requests.get(title_link)
    soup = BeautifulSoup(page.content, 'html.parser')

    verdict_div = soup.find('div', class_='verdict')
    if not verdict_div:
        return ''
    else:
        content_div = verdict_div.find('div', class_='content')
        if not content_div:
            return ''
        else:
            h2_element = content_div.find('h2')
            if h2_element:
                h2_text = h2_element.get_text(strip=True)
                return h2_text
            else:
                return ''


def try_find_claim_in_new_page(title_link):
    page = requests.get(title_link)
    soup = BeautifulSoup(page.content, 'html.parser')

    teza_div = soup.find('div', class_='teza')
    if teza_div:
        content_div = teza_div.find('div', class_='content')
        if content_div:
            text_content = content_div.get_text(strip=True)
            return text_content
        else:
            return ''
    else:
        return ''


def get_debunk_content(data_object):
    page = requests.get(data_object.debunking_link)
    soup = BeautifulSoup(page.content, 'html.parser')

    post_content_div = soup.find('div', class_='post-content')
    if post_content_div:
        first_p = post_content_div.find('p')
        if first_p:
            first_p_text = first_p.get_text(strip=True)
        else:
            first_p_text = ""

        concatenated_text = ""
        for p in post_content_div.find_all('p')[1:]:
            if p.get_text(strip=True) == 'Sources' or p.get_text(strip=True) == 'Source':
                # de aici sunt surse
                break
            concatenated_text += p.get_text(strip=True) + " "

        data_object.debunking_argument = concatenated_text
        data_object.fake_news_content = first_p_text
    else:
        return

def crawl_summary_page(p):
    print(p)
    page = requests.get(p)
    soup = BeautifulSoup(page.content, 'html.parser')

    posts = soup.find_all('div', class_='news-post')

    for post in posts:
        data_object = DataObject('fakenews_pl', 'https://fakenews.pl/en')

        title_tag = post.find('div', class_='post-title').find('a')
        title_text = title_tag.text.strip()
        title_link = title_tag['href']
        short_description = post.find('div', class_='post-content').p.get_text(strip=True)

        label_span = post.find('span', class_='labelocena')


        if label_span:
            verdict = label_span.text.strip()
        else:
            verdict = try_find_verdict_in_new_page(title_link)
            if verdict == '':
                continue
        if verdict != 'Satyra' and verdict != 'Analysis':
            # print(verdict)
            data_object.verdict = verdict
        else:
            continue
        claim = try_find_claim_in_new_page(title_link)
        if claim != '':
            data_object.statement = claim
        elif title_text != '':
            data_object.statement = title_text
        else:
            continue
        data_object.debunking_link = title_link
        data_object.summary_explanation = short_description
        data_object.spread_location = ['Poland']

        post_tags_ul = post.find('ul', class_='post-tags')
        date_li = post_tags_ul.find('li')
        date_text = date_li.get_text(strip=True)
        data_object.date = date_text
        get_debunk_content(data_object)

        author_li = post_tags_ul.find('li').find_next_sibling('li')
        author_name = author_li.get_text(strip=True).replace("by", "", 1).strip()
        data_object.journalist_name = author_name

        # queue.send_message(json.dumps(data_object.json_encoder()))
        localState.append(data_object)


        # print("Titlu:", title_text)
        # print("Link:", title_link)
        # print("Descriere:", short_description)
        #

    pages = soup.find('ul', class_="pagination-list")
    if pages:
        active_page = pages.find('a', class_="active")
        next_page = active_page.parent.find_next_sibling('li')
        if next_page is not None:
            next_link = next_page.find('a', class_='page-number')
            if next_link is not None and next_link['href']:
                next_link = next_link['href']
                crawl_summary_page(next_link)
    hrefs = []


#Starting at the base link the recursive crawling of each page
if __name__ == '__main__':
    pages = ['https://fakenews.pl/en/politics/','https://fakenews.pl/en/general/','https://fakenews.pl/en/health/']
    crawl_summary_page(pages[0])
    crawl_summary_page(pages[1])
    crawl_summary_page(pages[2])

