import pandas as pd
import time
import multiprocessing
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

CHROMEDRIVER_PATH = r'C:\Users\Kipplouser1\Desktop\gmaps\chromedriver.exe'
MAPS_LINK = 'https://www.google.com/maps'
df = pd.read_csv('keywords.csv')
format_company = df['company'].to_list()


def main_scrape(keywords):
    """This method reads a keyword from a csv file, searches for it on
     Google Maps and then extract all the relevant information
     """
    options = Options()
    user_agent = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.37")')
    options.add_argument(f'--user-agent={user_agent}')
    window_width = 1200
    window_height = 720
    options.add_argument(f'--window-size={window_width},{window_height}')
    s = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=s, options=options)
    # print('googleMapsScraper starting..')
    driver.get(MAPS_LINK)
    timeout = 10
    try:
        maps_page = EC.presence_of_element_located((By.ID, 'main'))
        WebDriverWait(driver, timeout).until(maps_page)
    except TimeoutException:
        print("Timed out! Waiting for page to re-load")

    try:
        search_box = driver.find_element(By.XPATH,
                                        '//*[@id="searchboxinput"]')
        search_box.click()
        for key in keywords:
            search_box.send_keys(key)
            search_button = driver.find_element(By.XPATH,
                                '//*[@id="searchbox-searchbutton"]')
            search_button.click()
    finally:
        print('searching maps..')
        try:
            driver.implicitly_wait(1)
            title = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH,
                '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/\
                div[2]/div/div[1]/div[1]/h1')))

            # title = driver.find_element(By.XPATH,
            #         '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/\
            #         div[1]/div/div/div[2]/div/div[1]/div[1]/h1')
            title = title.text
        except NoSuchElementException:
            title = 'NA'
        try:
            company_category = driver.find_element(By.XPATH,
            '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/\
                div/div[2]/div/div[1]/div[2]/div/div[2]/span/span/button')
            company_category = company_category.text
        except NoSuchElementException:
            company_category = 'NA'
        try:
            rating = driver.find_element(By.XPATH,
                '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/\
                div/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/span[1]/span[1]')
            rating = rating.text
        except NoSuchElementException:
            rating = 'NA'
        try:
            address = driver.find_element(By.XPATH,
                '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/\
                div/div[7]/div[3]/button/div/div[2]/div[1]')
            address = address.text
        except NoSuchElementException:
            address = 'NA'
        try:
            plus_codes = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".Io6YTe")))
            plus_codes = driver.find_element(By.CSS_SELECTOR, ".Io6YTe")
            plus_codes = plus_codes.text
        except NoSuchElementException:
            plus_codes = 'NA'
        try:
            website = driver.find_element(By.XPATH,
                '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/\
                div/div[7]/div[5]/a/div/div[2]/div[1]')
            website = website.text
        except NoSuchElementException:
            website = 'NA'
        try:
            phone_number = driver.find_element(By.XPATH,
                '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div\
                 /div/div[7]/div[7]/button/div/div[2]/div[1]')
            phone_number = phone_number.text
        except NoSuchElementException:
            phone_number = 'NA'

        time.sleep(3)
        driver.quit()

    # saving the extracted data in csv
    with open('file.csv', "a", encoding="utf-8") as fi:
        fi.write(
            f'"""{title}""",{company_category},{rating},"""{address}""","{website}","{plus_codes}","{phone_number}"\n')


if __name__ == "__main__":
    df = pd.read_csv('keywords.csv')
    keywords = df['company'].str.replace(' ', '+').str.replace(',',
                                                               '').to_list()
    num_processes = 8
    pool = multiprocessing.Pool(num_processes)

    # applying function to each keyword
    pool.map(main_scrape, keywords)

    # Close the pool
    pool.close()
    pool.join()
