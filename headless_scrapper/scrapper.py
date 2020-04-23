from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def get_browser():
    user_agent = '''
    Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36
    '''
    options = webdriver.ChromeOptions()
#    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('user-agent={0}'.format(user_agent))
    return webdriver.Chrome(ChromeDriverManager().install(), options=options)


def connect_to_page(browser, page):
    browser.get(page)
    browser.find_element_by_id('search_form_input_homepage').send_keys("realpython")
    browser.find_element_by_id("search_button_homepage").click()
    print(browser.current_url)
    browser.quit()


if __name__ == "__main__":
    page = 'https://www.educative.io/courses/python-201-interactively-learn-advanced-concepts-in-python-3'
    page = 'https://duckduckgo.com'
    browser = get_browser()
    connect_to_page(browser=browser)
