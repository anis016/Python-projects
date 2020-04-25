from selenium import webdriver
import configure
import random

user_agent = random.choice(configure.USER_AGENT_LIST)
headers = {'user-agent': user_agent}

driver_path = configure.get_chrome_driver()
options = webdriver.ChromeOptions()
options.add_argument('user-agent={0}'.format(user_agent))
driver = webdriver.Chrome(executable_path=driver_path)

driver.get('https://www.educative.io/courses/learn-dart-first-step-to-flutter')
# driver.find_element_by_id('search_form_input_homepage').send_keys("hello world")
# driver.find_element_by_id("search_button_homepage").click()
input("press any key to quit")
driver.quit()
