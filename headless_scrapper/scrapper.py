from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from configure import get_user_agent
from configure import get_proxies
from configure import get_chrome_driver
import json
from collections import defaultdict
import time
import requests
import random
from itertools import cycle
import pickle
from datetime import date
import random

user_agent, headers = get_user_agent("https://www.educative.io")


def get_browser(proxy=False):
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    # options.add_argument('user-agent={0}'.format(user_agent))
    if proxy:
        options.add_argument('--proxy-server={0}'.format(proxy))
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
    title = page.split("/")[-1]
    browser.get(page)
    time.sleep(3)
    browser.find_element_by_xpath('//*[@id="app"]/div[1]/div[3]/nav/div[3]/button[2]/span').click()
    browser.find_element_by_id('loginform-email').send_keys(email)
    browser.find_element_by_id('loginform-password').send_keys(password)
    browser.find_element_by_id("modal-login").click()
    time.sleep(5)
    content_download = defaultdict(dict)
    chapters = browser.find_elements_by_xpath('//*[@id="collection-tabs-pane-1"]/div')
    try:
        for chapter_id, chapter in enumerate(chapters, 1):
            chapter_title = chapter.text.split("\n")[0]
            chapter_contents_xpath = '//*[@id="collection-tabs-pane-1"]/div[{0}]/menu/div'.format(chapter_id)
            chapter_contents = chapter.find_elements_by_xpath(chapter_contents_xpath)
            content_links = dict()
            print("adding chapter: " + chapter_title)
            for content_id, content in enumerate(chapter_contents, 1):
                content_title = content.text
                content_xpath = '//*[@id="collection-tabs-pane-1"]/div[{0}]/menu/div[{1}]/a'.format(chapter_id, content_id)
                content_link = content.find_element_by_xpath(content_xpath).get_attribute('href')
                content_links[content_title] = content_link
                print("added content link: " + content_link)
            content_download[chapter_title] = content_links
            time.sleep(3)

        with open(title, 'w') as fw:
            fw.write(json.dumps(content_download))

        # serialize and save the content_download for later use
        content_filename = '{0}-{1}.pkl'.format(title, str(date.today()))
        with open(content_filename, 'wb') as handle:
            pickle.dump(json.dumps(content_download), handle, protocol=pickle.HIGHEST_PROTOCOL)
    finally:
        browser.quit()


if __name__ == "__main__":
    # page = 'https://www.educative.io/courses/learn-dart-first-step-to-flutter'
    page = "https://www.educative.io/courses/python-201-interactively-learn-advanced-concepts-in-python-3"

    # TODO: get fast and secure proxy and also resolve proxy wth no internet
    # proxies = get_proxies()
    # print("got {0} proxies".format(len(proxies)))
    # proxy_pool = cycle(proxies)
    # proxy = ""
    # for count, _ in enumerate(proxies, 1):
    #     proxy = next(proxy_pool)
    #     print("Request #{0} for proxy {1}".format(count, proxy))
    #     try:
    #         response = requests.get(page, proxies={"http": proxy, "https": proxy}, headers=headers, timeout=10.0)
    #         print("got a proxy.. breaking")
    #         break
    #     except Exception as exception:
    #         print("Skipping. Connection error")
    #     print()

    browser = get_browser(proxy=False)
    get_page_contents(browser=browser, page=page)
