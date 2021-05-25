import time
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome()
driver.get('https://mail.ru/')

login = driver.find_element_by_name('login')
login.send_keys('study.ai_172@mail.ru')
login.send_keys(Keys.ENTER)

password = WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.NAME, "password")))
password.send_keys('NextPassword172!')
password.send_keys(Keys.ENTER)

time.sleep(5)

all_links = set()
time.sleep(3)
mail_list = driver.find_elements_by_xpath("//div[@class='dataset__items']/a[@href]")
link_list = list(map(lambda el: el.get_attribute('href'), mail_list))
all_links = all_links.union(set(link_list))

while True:
    actions = ActionChains(driver)
    actions.move_to_element(mail_list[-1])
    actions.perform()

    time.sleep(3)
    mail_list = driver.find_elements_by_xpath("//div[@class='dataset__items']/a[@href]")
    link_list = list(map(lambda el: el.get_attribute('href'), mail_list))

    if link_list[-1] not in all_links:
        all_links = all_links.union(set(link_list))
        continue
    else:
        break

message_list = []
for some_data in all_links:
    time.sleep(5)
    driver.get(some_data)
    time.sleep(5)
    message_dict = {}
    message_dict['name'] = driver.find_element_by_xpath("//div[@class='letter__author']/span[@class='letter-contact']").text
    message_dict['time'] = driver.find_element_by_xpath("//div[@class='letter__author']/div[@class='letter__date']").text
    message_dict['theme'] = driver.find_element_by_xpath("//h2[@class='thread__subject']").text
    message_dict['main'] = driver.find_element_by_xpath("//div[@class='html-expander']").text
    message_list.append(message_dict)
print(message_list)

driver.close()

