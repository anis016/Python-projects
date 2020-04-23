from selenium import webdriver
import configure

driver_path = configure.get_chrome_driver()
driver = webdriver.Chrome(executable_path=driver_path)

driver.get("https://duckduckgo.com/")
driver.find_element_by_id('search_form_input_homepage').send_keys("hello world")
driver.find_element_by_id("search_button_homepage").click()
input("press any key to quit")
driver.quit()
