import json
import sys

from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import tldextract
from bs4 import BeautifulSoup
import csv

from QueueConnectionModule import QueueConnectionModule
from country_domain_name import get_first_country_by_suffix, get_country_by_unique_language, \
    get_first_country_by_domain_name
from country_languages import *

from DataObject import DataObject
from LocalState import LocalState
from scrapers.BaseScraper import BaseScraper

#localState = LocalState(db_filename='euvsdisinfo_local_state.csv', faulty_filename='euvsdisinfo_faulty.csv')
#queue = QueueConnectionModule()
index = 0
class EuvsdisinfoScraper(BaseScraper):
    def __int__(self, db_filename='euvsdisinfo_local_state.csv', faulty_filename='euvsdisinfo_faulty.csv'):
        BaseScraper.__init__(self, db_filename, faulty_filename)
    def get_summary(self, driver):
        summaries = driver.find_elements(By.CSS_SELECTOR, '.b-report__summary .b-text p')
        summary = ''
        for summ in summaries:
            summary += summ.text.strip()

        return summary


    def get_response(self, driver):
        responses = driver.find_elements(By.CSS_SELECTOR, '.b-report__response .b-text p')
        response = ''
        for r in responses:
            response += r.text.strip()

        return response


    def get_fake_news_outlets(self, driver):
        first_li = driver.find_element(By.CSS_SELECTOR, '.b-report__details-list > li')

        # În interiorul acestui <li>, găsește toate elementele <a>
        all_a_elements = first_li.find_elements(By.TAG_NAME, 'a')

        # Extrage valorile href din fiecare element <a>
        hrefs = [a.get_attribute('href') for a in all_a_elements if 'archived' not in a.text]
        texts = [a.text for a in all_a_elements if 'archived' not in a.text]
        return hrefs, texts


    def get_article_language(self, driver, url):
        li_elements = driver.find_elements(By.XPATH,
                                           "//ul[@class='b-report__details-list']//li[contains(text(), 'Article language(s):')]")

        if li_elements:
            li_with_text = li_elements[0]

        else:
            li_elements = driver.find_elements(By.XPATH,
                                               "//ul[@class='b-report__details-list']//li[contains(text(), 'Outlet language(s):')]")
            if li_elements:
                li_with_text = li_elements[0]
            else:
                return []

        # În interiorul acestui <li>, găsește elementul <span>
        span_element = li_with_text.find_element(By.TAG_NAME, 'span').text
        list_languages = span_element.split(',')
        final_lang_list = []
        for lang in list_languages:
            ll = lang.lower().strip()
            final_lang_list.append(ll)

        return final_lang_list


    def get_tags(self, driver):
        keywords_div = driver.find_element(By.CSS_SELECTOR, '.b-report__keywords')
        all_span_elements = keywords_div.find_elements(By.TAG_NAME, 'span')
        tags = [span.text.strip() for span in all_span_elements]
        return tags

    def get_location_from_sources(self, sources):
        list_countries = []
        for source in sources:
            res = tldextract.extract(source)
            res_suffix = res.suffix
            country = get_first_country_by_suffix(res_suffix)
            if country:
                list_countries.append(country)
            res_subdomain = res.subdomain
            country = get_first_country_by_suffix(res_subdomain)
            if country:
                list_countries.append(country)
            res_domain = res.domain
            country = get_first_country_by_domain_name(res_domain)
            if country:
                list_countries.append(country)
        return list_countries

    def get_location_unique_language(self, languages):
        list_countries = []
        for lang in languages:
            country = get_country_by_unique_language(lang)
            if country:
                list_countries.append(country)
        return list_countries

    def get_spread_location(self, data_object, outlet_texts):
        locations = self.get_location_from_sources(data_object.fake_news_source)
        locations.extend(self.get_location_unique_language(data_object.languages))
        for text in outlet_texts:
            country = get_first_country_by_domain_name(text.lower())
            if country:
                locations.append(country)
        locations = list(set(locations))
        return locations

    def parse_debunk_page(self, data_object):
        browser_options = ChromeOptions()
        browser_options.headless = True

        driver = Chrome(options=browser_options)

        driver.get(data_object.debunking_link)
        data_object.fake_news_content = self.get_summary(driver)
        data_object.debunking_argument = self.get_response(driver)
        data_object.fake_news_source, outlet_texts = self.get_fake_news_outlets(driver)
        data_object.languages = self.get_article_language(driver, data_object.debunking_link)
        data_object.spread_location = self.get_spread_location(data_object, outlet_texts)
        data_object.tags = self.get_tags(driver)

        driver.close()


    def get_statement(self, soup):
        title = soup.select_one('.b-archive__database-item-title').get_text(strip=True)

        if title.startswith("DISINFO:"):
            cleaned_title = title.replace("DISINFO:", "").strip()
        else:
            cleaned_title = title

        return cleaned_title

    def complete_info(self, data_obj):
        """
        Check if the object is complete and ready to be sent.
        This validation is done in order to reduce faulty data inserted in the system
        """
        if data_obj.statement is None or data_obj.statement.strip() == '':
            return False
        if data_obj.fake_news_source == []:
            return False
        if data_obj.spread_location == []:
            return False
        if data_obj.languages == []:
            return False
        if data_obj.tags == []:
            return False
        if data_obj.debunking_link is None or data_obj.debunking_link.strip() == '':
            return False
        return True

    def crawl_summary_page(self, url, rescrape_faulty=False, updates_only=False):
        global index
        browser_options = ChromeOptions()
        browser_options.headless = True

        driver = Chrome(options=browser_options)
        driver.get(url)

        news = driver.find_elements(By.CSS_SELECTOR, '.b-archive__database-item')


        for n in news:
            link = n.get_attribute('href').strip()
            if ((not rescrape_faulty and not self.local_state.already_parsed(link))
                    or (rescrape_faulty and self.local_state.has_faulty(link))):
                if rescrape_faulty and self.manual_inputted_data(link, rescrape_faulty):
                    continue
                data_object = DataObject('EuVsDisInfo', 'https://euvsdisinfo.eu/disinformation-cases/')
                element_html = n.get_attribute('innerHTML')
                soup = BeautifulSoup(element_html, 'html.parser')

                data_object.statement = self.get_statement(soup)
                data_object.date = soup.select_one('.b-archive__database-item-date').get_text(strip=True)
                data_object.debunking_link = n.get_attribute('href').strip()
                try:
                    self.parse_debunk_page(data_object)
                    index += 1
                    if not self.complete_info(data_object):
                        self.local_state.append_faulty(data_object)
                        continue
                    self.send_data(data_object, False)
                except Exception as e:
                    print(f"A avut o eroare {e}")
                    self.local_state.append_faulty(data_object)
                print(index)
                index = index + 1

        try:
            pagination_div = driver.find_element(By.CSS_SELECTOR, '.b-pagination')
            items = pagination_div.find_elements(By.CSS_SELECTOR, '.b-pagination__item')
        except Exception as e:
            print(f"A avut o eroare {e}")
            print(f"final de algo {index}")
            exit(0)

        # Identifică indexul paginii curente
        current_index = None
        for idx, item in enumerate(items):
            if "current" in item.get_attribute("class"):
                current_index = idx
                break

        # Verifică dacă există pagini ulterioare și extrage link-ul
        next_page_link = ''
        if current_index is not None and current_index < len(items) - 1:
            next_item = items[current_index + 1]
            # Verifică dacă elementul următor este un link și extrage link-ul
            if next_item.tag_name == "a":
                next_page_link = next_item.get_attribute('href')

        print(next_page_link)
        with open('pages.txt', 'a') as file:
            file.write(next_page_link + "\n")

        if next_page_link != '':
            driver.close()
            self.crawl_summary_page(next_page_link, rescrape_faulty, updates_only)

        driver.quit()


if __name__ == '__main__':
    euvsdisinfo_scraper = EuvsdisinfoScraper(db_filename='euvsdisinfo_local_state.csv', faulty_filename='euvsdisinfo_faulty.csv')
    main_page = "https://euvsdisinfo.eu/disinformation-cases/"
    if len(sys.argv) < 2:
        print("run this program with arguments: scrape_all, rescrape_faulty, updates_only")
    if sys.argv[1] == "scrape_all":
        euvsdisinfo_scraper.crawl_summary_page(main_page)
    elif sys.argv[1] == "rescrape_faulty":
        euvsdisinfo_scraper.crawl_summary_page(main_page, rescrape_faulty=True)
    elif sys.argv[1] == "updates_only":
        euvsdisinfo_scraper.crawl_summary_page(main_page, rescrape_faulty=False, updates_only=True)
    #crawl_summary_page("https://euvsdisinfo.eu/disinformation-cases/page/117/")
    # crawl_summary_page("https://euvsdisinfo.eu/disinformation-cases/page/4/")
