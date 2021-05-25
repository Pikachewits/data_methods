from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(options=chrome_options)

driver.get('https://www.mvideo.ru/')

items = []

for i in range(5):
    button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//h2[contains(text(), 'Новинки')]/ancestor::div[@class='section']//a[contains(@class, 'i-icon-fl-arrow-right')]")))
    button.click()

goods = driver.find_elements_by_xpath("//h2[contains(text(), 'Новинки')]/ancestor::div[@class='section']//a[@class = 'fl-product-tile-title__link sel-product-tile-title']")
for g in goods:
    if g not in items:
        items.append(g)

for product in items:
    print(product.get_attribute('data-product-info'))

driver.close()