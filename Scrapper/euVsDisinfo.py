from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from country_languages import *

from kg_repo.Scrapper.DataObject import DataObject
from kg_repo.Scrapper.LocalState import LocalState

localState = LocalState()


def get_summary(driver):
    summaries = driver.find_elements(By.CSS_SELECTOR, '.b-report__summary .b-text p')
    summary = ''
    for summ in summaries:
        summary += summ.text.strip()

    return summary


def get_response(driver):
    responses = driver.find_elements(By.CSS_SELECTOR, '.b-report__response .b-text p')
    response = ''
    for r in responses:
        response += r.text.strip()

    return response


def get_fake_news_outlets(driver):
    first_li = driver.find_element(By.CSS_SELECTOR, '.b-report__details-list > li')

    # În interiorul acestui <li>, găsește toate elementele <a>
    all_a_elements = first_li.find_elements(By.TAG_NAME, 'a')

    # Extrage valorile href din fiecare element <a>
    hrefs = [a.get_attribute('href') for a in all_a_elements if 'archived' not in a.text]

    return hrefs


def get_article_language(driver, url):
    li_elements = driver.find_elements(By.XPATH,
                                       "//ul[@class='b-report__details-list']//li[contains(text(), 'Article language(s):')]")

    if li_elements:
        li_with_text = li_elements[0]
    else:
        return []

    # În interiorul acestui <li>, găsește elementul <span>
    span_element = li_with_text.find_element(By.TAG_NAME, 'span').text
    list_languages = span_element.split(',')
    list_countries = []
    for lang in list_languages:
        list_countries.append(get_first_country_by_language(lang.strip(), url))

    return list_countries


def get_tags(driver):
    keywords_div = driver.find_element(By.CSS_SELECTOR, '.b-report__keywords')
    all_span_elements = keywords_div.find_elements(By.TAG_NAME, 'span')
    tags = [span.text.strip() for span in all_span_elements]

    return tags


def parse_debunk_page(data_object):
    browser_options = ChromeOptions()
    browser_options.headless = True

    driver = Chrome(options=browser_options)

    driver.get(data_object.debunking_link)
    data_object.fake_news_content = get_summary(driver)
    data_object.debunking_argument = get_response(driver)
    data_object.fake_news_source = get_fake_news_outlets(driver)
    data_object.spread_location = get_article_language(driver, data_object.debunking_link)
    data_object.tags = get_tags(driver)


def get_statement(n):
    title = n.find_element(By.CSS_SELECTOR, '.b-archive__database-item-title').text.strip()
    if title.startswith("DISINFO:"):
        cleaned_title = title.replace("DISINFO:", "").strip()
    else:
        cleaned_title = title

    return cleaned_title


def crawl_summary_page(url):
    browser_options = ChromeOptions()
    browser_options.headless = True

    driver = Chrome(options=browser_options)
    driver.get(url)

    news = driver.find_elements(By.CSS_SELECTOR, '.b-archive__database-item')
    data = []
    for n in news:
        if not localState.already_parsed(n.get_attribute('href').strip()):
            data_object = DataObject('EuVsDisInfo', 'https://euvsdisinfo.eu/disinformation-cases/')
            data_object.statement = get_statement(n)
            data_object.date = n.find_element(By.CSS_SELECTOR, '.b-archive__database-item-date').text.strip()
            data_object.debunking_link = n.get_attribute('href').strip()
            parse_debunk_page(data_object)
            localState.append(data_object)

    pagination_div = driver.find_element(By.CSS_SELECTOR, '.b-pagination')
    items = pagination_div.find_elements(By.CSS_SELECTOR, '.b-pagination__item')

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
    if next_page_link != '':
        crawl_summary_page(next_page_link)

    driver.quit()


if __name__ == '__main__':
    crawl_summary_page("https://euvsdisinfo.eu/disinformation-cases/")
    # crawl_summary_page("https://euvsdisinfo.eu/disinformation-cases/page/4/")
