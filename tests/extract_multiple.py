import os
import re
import time
import multiprocessing
import traceback
import pandas as pd
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


CHROMEDRIVER_PATH = r'C:\Users\Kipplouser1\Desktop\maps\chromedriver.exe'
MAPS_LINK = 'https://www.google.com/maps'


options = Options()
user_agent = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
              '(KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.37")')
options.add_argument(f'--user-agent={user_agent}')

options.add_argument('--start-maximized')

driver = webdriver.Chrome()
driver.get(MAPS_LINK)
time.sleep(3)

try:
    maps_page = EC.presence_of_element_located((By.XPATH, '//*[@id="searchboxinput"]')) 
    WebDriverWait(driver, 10).until(maps_page)
    
    search_box = driver.find_element(By.XPATH,
                                     '//*[@id="searchboxinput"]')
    search_box.click()
    search_box.send_keys('m.Isabel Photography')    # keyword to search for 
    search_button = driver.find_element(By.XPATH,
                                        '//*[@id="searchbox-searchbutton"]')
    search_button.click()
except:
    pass

time.sleep(10)


try:
    title = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH,
            '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[1]/h1')))
    title = title.text
    print(f'Found "{title}"... extracting the rest of the data')
except selenium.common.exceptions.TimeoutException:
    print('Title time out')
    

wait = WebDriverWait(driver, 60)  
elements = wait.until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR,  '.CsEnBe')))


# elements = driver.find_elements(By.CSS_SELECTOR, '.CsEnBe')

for element in elements:
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    aria_label = element.get_attribute("aria-label")
    # print(aria_label)

    pattern = r'(\w+): ([^\n]+)'
    matches = re.findall(pattern, aria_label)
    key_value_pairs = dict(matches)
    # print(key_value_pairs)

    for key, value in key_value_pairs.items():
        if key == 'Address':
            address = value
        if key == 'Website':
            website = value
        if key == 'Phone':
            phone = value
        if key == 'code':
            code = value


with open('file234.csv', "a", encoding="utf-8") as fi:
    fi.write(f'"{address}",{website},{phone},"{code}"\n')
    






  