import sys
import requests
from bs4 import BeautifulSoup

from DataObject import DataObject
from openAI import FakeNewsChannelIdentifier
from scrapers.BaseScraper import BaseScraper

index = 0
total_empty = 0


class FakenewsPLScraper(BaseScraper):
    def complete_info(self, data_obj: DataObject):
        if data_obj.statement is None or data_obj.statement.strip() == '':
            return False
        if data_obj.summary_explanation.strip() == '':
            return False
        if data_obj.date.strip() == '':
            return False
        if data_obj.debunking_argument.strip() == '':
            return False
        if data_obj.fake_news_content.strip() == '':
            return False
        if data_obj.debunking_link is None or data_obj.debunking_link.strip() == '':
            return False
        if not data_obj.fake_news_source or "" in data_obj.fake_news_source:
            return False
        return True

    def __int__(self, db_filename='fakenewsPL_local_state.csv', faulty_filename='fakenewsPL_faulty.csv'):
        BaseScraper.__init__(self, db_filename, faulty_filename)

    def extract_name(self, soup):
        image = soup.find('img', 'rounded-circle img-fluid')
        if image != None:
            return image["alt"]
        return ""

    def try_find_verdict_in_new_page(self, title_link):
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

    def try_find_claim_in_new_page(self, title_link):
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

    def get_debunk_content(self, data_object):
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

    def crawl_summary_page(self, p, rescrape_faulty=False, updates_only=False):
        global index, total_empty
        print(p)
        page = requests.get(p)
        soup = BeautifulSoup(page.content, 'html.parser')

        posts = soup.find_all('div', class_='news-post')

        for post in posts:
            # data_object = DataObject('fakenews_pl', 'https://fakenews.pl/en')
            data_object = DataObject('fakenews_pl', 'https://fakenews.pl/en')

            title_tag = post.find('div', class_='post-title').find('a')
            title_text = title_tag.text.strip()
            title_link = title_tag['href']
            if ((not rescrape_faulty and not self.local_state.already_parsed(title_link)) or
                    (rescrape_faulty and self.local_state.has_faulty(title_link)) or
                    updates_only):
                if updates_only and (
                        self.local_state.has_faulty(title_link) or self.local_state.already_parsed(title_link)):
                    print("Finish updates")
                    exit(0)
                if rescrape_faulty and self.manual_inputted_data(title_link, rescrape_faulty):
                    continue

                short_description = post.find('div', class_='post-content').p.get_text(strip=True)

                label_span = post.find('span', class_='labelocena')

                if label_span:
                    verdict = label_span.text.strip()
                else:
                    verdict = self.try_find_verdict_in_new_page(title_link)
                    if verdict == '':
                        continue
                if verdict != 'Satyra' and verdict != 'Analysis':
                    # print(verdict)
                    data_object.verdict = verdict
                else:
                    continue
                claim = self.try_find_claim_in_new_page(title_link)
                if claim != '':
                    data_object.statement = claim
                elif title_text != '':
                    data_object.statement = title_text
                else:
                    continue
                data_object.debunking_link = title_link
                data_object.summary_explanation = short_description
                data_object.spread_location = ['Poland']
                data_object.languages = ['Polish']

                post_tags_ul = post.find('ul', class_='post-tags')
                date_li = post_tags_ul.find('li')
                date_text = date_li.get_text(strip=True)
                data_object.date = date_text
                self.get_debunk_content(data_object)

                author_li = post_tags_ul.find('li').find_next_sibling('li')
                author_name = author_li.get_text(strip=True).replace("by", "", 1).strip()
                data_object.journalist_name = author_name
                self.getSpreadSource(data_object)


                if self.complete_info(data_object):
                    self.send_data(data_object, rescrape_faulty)
                else:
                    self.local_state.append_faulty(data_object)
                    total_empty += 1
                index = index + 1
                print(index)
                print(total_empty)

        pages = soup.find('ul', class_="pagination-list")
        if pages:
            active_page = pages.find('a', class_="active")
            next_page = active_page.parent.find_next_sibling('li')
            if next_page is not None:
                next_link = next_page.find('a', class_='page-number')
                if next_link is not None and next_link['href']:
                    next_link = next_link['href']
                    self.crawl_summary_page(next_link, rescrape_faulty, updates_only)
        hrefs = []

    def getSpreadSource(self, data_object):
        identifier = FakeNewsChannelIdentifier()
        fake_news_channel, debunk_channel = identifier.identify_channels(data_object.debunking_argument)
        for chanel in debunk_channel:
            if chanel == 'example website':
                print("Am avut example")
                return

        if 'example website' in debunk_channel:
            debunk_channel.remove('example website')
        if 'Social media (Facebook, Twitter)' in fake_news_channel:
            fake_news_channel.remove('Social media (Facebook, Twitter)')
            fake_news_channel.append('Facebook')
            fake_news_channel.append('Twitter')
        if 'fakenews.pl' in debunk_channel:
            debunk_channel.remove('fakenews.pl')
        if 'fakenews.pl' in fake_news_channel:
            fake_news_channel.remove('fakenews.pl')

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
    fakenewsPLScraper = FakenewsPLScraper(db_filename='fakenewsPL_local_state.csv',
                                         faulty_filename='fakenewsPL_faulty.csv')
    if len(sys.argv) < 2:
        print("run this program with arguments: scrape_all, rescrape_faulty, updates_only")
    if sys.argv[1] == "scrape_all":
        pages = ['https://fakenews.pl/en/politics/', 'https://fakenews.pl/en/general/',
                 'https://fakenews.pl/en/health/']
        fakenewsPLScraper.crawl_summary_page(pages[0])
        fakenewsPLScraper.crawl_summary_page(pages[1])
        fakenewsPLScraper.crawl_summary_page(pages[2])
    elif sys.argv[1] == "rescrape_faulty":
        pages = ['https://fakenews.pl/en/politics/', 'https://fakenews.pl/en/general/',
                 'https://fakenews.pl/en/health/']
        fakenewsPLScraper.crawl_summary_page(pages[0], rescrape_faulty=True)
        fakenewsPLScraper.crawl_summary_page(pages[1], rescrape_faulty=True)
        fakenewsPLScraper.crawl_summary_page(pages[2], rescrape_faulty=True)
    elif sys.argv[1] == "updates_only":
        pages = ['https://fakenews.pl/en/politics/', 'https://fakenews.pl/en/general/',
                 'https://fakenews.pl/en/health/']
        fakenewsPLScraper.crawl_summary_page(pages[0], rescrape_faulty=False, updates_only=True)
        fakenewsPLScraper.crawl_summary_page(pages[1], rescrape_faulty=False, updates_only=True)
        fakenewsPLScraper.crawl_summary_page(pages[2], rescrape_faulty=False, updates_only=True)
