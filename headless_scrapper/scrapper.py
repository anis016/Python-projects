from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from configure import USER_AGENT_LIST
from configure import get_proxies
from configure import get_chrome_driver
import json
from collections import defaultdict
import time
import requests
import random
import pickle
from datetime import date
import random

user_agent = random.choice(USER_AGENT_LIST)
headers = {'user-agent': user_agent}


def get_browser():
    # TODO: get fast and secure proxy and also resolve proxy wth no internet
    # proxy = random.choice(list(get_proxies()))
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('user-agent={0}'.format(user_agent))
    # options.add_argument('--proxy-server=http://{0}'.format(proxy))
    driver_path = get_chrome_driver()
    return webdriver.Chrome(executable_path=driver_path, options=options)


def sanitize_json(json_string):
    json_string = json_string.replace("\n", "")
    json_string = json_string.replace(",}", "}")
    json_string = json_string.replace(",]", "")
    return json_string.replace("\t", "")


def get_user_password():
    with open(".config", "r") as fr:
        data = fr.read()
        sanitized_data = sanitize_json(data)
        credentials = json.loads(sanitized_data)
        email = credentials['email']
        password = credentials['password']
    return email, password


def get_page_contents(browser, page):
    email, password = get_user_password()
    print(page)
    browser.get(page)
    browser.find_element_by_xpath('//*[@id="app"]/div[1]/div[3]/nav/div[3]/button[2]/span').click()
    browser.find_element_by_id('loginform-email').send_keys(email)
    browser.find_element_by_id('loginform-password').send_keys(password)
    browser.find_element_by_id("modal-login").click()

    input("press anything to continue")
    content_download = defaultdict(dict)
    chapters = browser.find_elements_by_xpath('//*[@id="collection-tabs-pane-1"]/div')
    for chapter_id, chapter in enumerate(chapters, 1):
        chapter_title = chapter.text.split("\n")[0]
        chapter_contents_xpath = '//*[@id="collection-tabs-pane-1"]/div[{0}]/menu/div'.format(chapter_id)
        chapter_contents = chapter.find_elements_by_xpath(chapter_contents_xpath)
        content_links = dict()
        print("adding downloadable for " + chapter_title)
        for content_id, content in enumerate(chapter_contents, 1):
            content_title = content.text
            content_xpath = '//*[@id="collection-tabs-pane-1"]/div[{0}]/menu/div[{1}]/a'.format(chapter_id, content_id)
            content_link = content.find_element_by_xpath(content_xpath).get_attribute('href')
            content_links[content_title] = content_link
            print("added title: " + content_link + "link: " + content_link)
        content_download[chapter_title] = content_links
        time.sleep(3)
    browser.quit()
    # serialize and save the content_download for later use
    content_filename = '{0}-{1}.pkl'.format(page, date)
    with open(content_filename, 'wb') as handle:
        pickle.dump(content_download, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    page = 'https://www.educative.io/courses/learn-dart-first-step-to-flutter'
    browser = get_browser()
    get_page_contents(browser=browser, page=page)
