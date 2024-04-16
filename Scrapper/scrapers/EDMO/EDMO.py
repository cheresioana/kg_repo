import locale
import sys
import re
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import DataObject
from ress import translateString, translate_object
from scrapers.BaseScraper import BaseScraper
from DataObject import DataObject
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By

index = 0
total_empty = 0
verdict_counts = {}


class EDMOScraper(BaseScraper):
    def __int__(self, db_filename='edmo_local_state.csv', faulty_filename='edmo_faulty.csv'):
        BaseScraper.__init__(self, db_filename, faulty_filename)

    def complete_info(self, data_obj: DataObject):
        if data_obj.statement is None or data_obj.statement.strip() == '':
            return False
        if data_obj.date.strip() == '':
            return False
        if not data_obj.languages:
            return False
        if data_obj.debunking_link is None or data_obj.debunking_link.strip() == '':
            return False
        return True

    def crawl_summary_page(self, page, rescrape_faulty=False, updates_only=False):
        languages_info = {
            # "nl": {"language": "Dutch", "country": "Netherlands"},
            # "de": {"language": "German", "country": ""},
            # "fr": {"language": "French", "country": "France"},
            # "en": {"language": "English", "country": ""},
            # "hu": {"language": "Hungarian", "country": "Hungary"},
            # "da": {"language": "Danish", "country": "Denmark"},
            # "pl": {"language": "Polish", "country": "Poland"},
            # "el": {"language": "Greek", "country": "Greece"},
            # "cs": {"language": "Czech", "country": "Czech Republic"},
            "no": {"language": "Norwegian", "country": "Norway"},
            "sk": {"language": "Slovak", "country": "Slovakia"},
            "ro": {"language": "Romanian", "country": "Romania"},
            "lb": {"language": "Luxembourgish", "country": "Luxembourg"},
            "hr": {"language": "Croatian", "country": "Croatia"},
            "lv": {"language": "Latvian", "country": "Latvia"},
            "bg": {"language": "Bulgarian", "country": "Bulgaria"},
            "et": {"language": "Estonian", "country": "Estonia"},
            "lt": {"language": "Lithuanian", "country": "Lithuania"},
            "sl": {"language": "Slovenian", "country": "Slovenia"},
        }

        global index, total_empty
        browser_options = ChromeOptions()
        browser_options.headless = True

        driver = Chrome(options=browser_options)
        driver.get(page)
        time.sleep(3)
        showMoreLanguages = driver.find_elements(By.XPATH,
                                                 "//div[contains(@class, 'filter__item') and .//div[contains(text(), 'Language')]]//button[contains(@class, 'css-1spymje')]")
        for s in showMoreLanguages:
            s.click()
        time.sleep(3)

        for cod, info in languages_info.items():
            checkbox = driver.find_element(By.XPATH,
                                           f"//div[contains(@class, 'filter__section')]//input[@value='{cod}']")
            if not checkbox.is_selected():  # Verifică dacă checkbox-ul nu este deja selectat
                checkbox.click()
            time.sleep(3)

            # while index < 2200:
            #     html_content = driver.page_source
            #     soup = BeautifulSoup(html_content, 'html.parser')
            #     posts = soup.find_all('div', class_='result__body')
            #     index += len(posts)
            #     next_page_button = driver.find_element(By.XPATH, "//button[@aria-label='Go to next page']")
            #     next_page_button.click()
            #     time.sleep(2)
            #     print(index)

            buttonsTranslate = driver.find_element(By.CLASS_NAME, 'css-1728t8k')
            while buttonsTranslate:
                try:
                    buttonsTranslate.click()
                    # Așteaptă un moment pentru ca acțiunea de click să fie procesată
                    time.sleep(1)
                    buttonsTranslate = driver.find_element(By.CLASS_NAME, 'css-1728t8k')
                    continue
                except:
                    # Dacă butonul nu poate fi apăsat, sări peste el
                    break
            time.sleep(1)
            html_content = driver.page_source

            soup = BeautifulSoup(html_content, 'html.parser')
            posts = soup.find_all('div', class_='result__body')

            for post in posts:
                data_object = DataObject('edmo', 'https://edmo-factchecks-filter.ilabhub.atc.gr/')
                headline = post.find('div', class_='result__headline').find('a')
                title = headline.get_text(strip=True)
                debunk_link = headline['href']
                data_object.statement = title
                data_object.debunking_link = debunk_link

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

                    feed_name_date = post.find('div', class_='result__feed-name_date')
                    data_object.date = self.convertDate(
                        feed_name_date.find('div', class_='result__release-date--text').get_text(strip=True))
                    shortDescription = post.find('div', class_='self-start')
                    if shortDescription:
                        shortDescription = shortDescription.get_text(strip=True)
                    else:
                        shortDescription = ''

                    data_object.summary_explanation = shortDescription
                    data_object.spread_location = [info['language']]
                    data_object.languages = [info['country']]

                    if self.complete_info(data_object):
                        self.send_data(data_object, rescrape_faulty)
                    else:
                        self.local_state.append_faulty(data_object)
                    print(index)
                    index += 1
            next_page_button = driver.find_element(By.XPATH, "//button[@aria-label='Go to next page']")
            while not "Mui-disabled" in next_page_button.get_attribute("class"):
                next_page_button.click()
                time.sleep(2)
                next_page_button = driver.find_element(By.XPATH, "//button[@aria-label='Go to next page']")
                buttonsTranslate = driver.find_elements(By.CLASS_NAME, 'css-1728t8k')
                try:
                    buton = buttonsTranslate[0]
                except:
                    pass
                num_buttons = len(buttonsTranslate)
                while buttonsTranslate:
                    try:
                        buton.click()
                        # Așteaptă un moment pentru ca acțiunea de click să fie procesată
                        time.sleep(1)
                        buttonsTranslate = driver.find_elements(By.CLASS_NAME, 'css-1728t8k')
                        if len(buttonsTranslate) == num_buttons:
                            try:
                                buton = buttonsTranslate[1]
                            except:
                                break
                        else:
                            try:
                                buton = buttonsTranslate[0]
                            except:
                                break

                        num_buttons = len(buttonsTranslate)
                        continue
                    except:
                        # Dacă butonul nu poate fi apăsat, sări peste el
                        break
                time.sleep(1)
                html_content = driver.page_source

                soup = BeautifulSoup(html_content, 'html.parser')
                posts = soup.find_all('div', class_='result__body')

                for post in posts:
                    data_object = DataObject('edmo', 'https://edmo-factchecks-filter.ilabhub.atc.gr/')
                    headline = post.find('div', class_='result__headline').find('a')
                    title = headline.get_text(strip=True)
                    debunk_link = headline['href']
                    data_object.statement = title
                    data_object.debunking_link = debunk_link

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

                        feed_name_date = post.find('div', class_='result__feed-name_date')
                        data_object.date = self.convertDate(feed_name_date.find('div', class_='result__release-date--text').get_text(strip=True))
                        shortDescription = post.find('div', class_='self-start')
                        if shortDescription:
                            shortDescription = shortDescription.get_text(strip=True)
                        else:
                            shortDescription = ''

                        data_object.summary_explanation = shortDescription
                        data_object.spread_location = [info['language']]
                        data_object.languages = [info['country']]

                        if self.complete_info(data_object):
                            self.send_data(data_object, rescrape_faulty)
                        else:
                            self.local_state.append_faulty(data_object)
                        print(index)
                        index += 1




            checkbox = driver.find_element(By.XPATH,
                                           f"//div[contains(@class, 'filter__section')]//input[@value='{cod}']")
            if checkbox.is_selected():  # Verifică dacă checkbox-ul nu este deja selectat
                checkbox.click()
            time.sleep(4)

        exit()

    def convertDate(self, date_str):
        input_format = "%d %b %Y"
        output_format = "%d.%m.%Y"

        date_obj = datetime.strptime(date_str, input_format)
        formatted_date = date_obj.strftime(output_format)

        return formatted_date


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
    EDMOScraper = EDMOScraper(db_filename='EDMO_local_state.csv',
                                        faulty_filename='EDMO_faulty.csv')

    pages = ['https://edmo-factchecks-filter.ilabhub.atc.gr/']

    if len(sys.argv) < 2:
        print("run this program with arguments: scrape_all, rescrape_faulty, updates_only")
    if sys.argv[1] == "scrape_all":
        for page in pages:
            EDMOScraper.crawl_summary_page(page)
    elif sys.argv[1] == "rescrape_faulty":
        for page in pages:
            EDMOScraper.crawl_summary_page(page, rescrape_faulty=True)
    elif sys.argv[1] == "updates_only":
        for page in pages:
            EDMOScraper.crawl_summary_page(page, rescrape_faulty=False, updates_only=True)