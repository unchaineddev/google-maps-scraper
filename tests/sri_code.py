import os
import re
import time
import multiprocessing
import traceback
import pandas as pd
# import requests
import selenium

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
# TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# from fake_useragent import UserAgent

CHROMEDRIVER_PATH = r'C:\Users\Administrator\Desktop\gmaps-scrape\driver\chromedriver.exe'
MAPS_LINK = 'https://www.google.com/maps'
timeout = 60
print('Starting Scraper')


def extract_information(driver):
    """
    extract all information in the page
    """
    global title, rating, address, website, phone, plus_code
    if not css_checker(driver):
        return
    else:
        print("CSS found for the page..extracting info!!")

    try:
        # Searching for the title
        title = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH,
                                              '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/\
                div[2]/div/div[1]/div[1]/h1')))
        title = title.text
        print(f'Found "{title}"... extracting the rest of the data')
    except selenium.common.exceptions.TimeoutException:
        print('Could not find the title!')
        skipping_dir = 'https://www.google.com/maps/dir/'
        missing_url = driver.current_url
        if skipping_dir in missing_url:
            print('skipping...')
            page_src = driver.page_source
            with open(f'C:\\Users\\Kipplouser1\\Desktop\\1409_final\\page_src\\{title}.html', 'w',
                      encoding='UTF-8') as f:
                f.writelines(page_src)
            driver.refresh()

    # if company title is present, scrapes rest of the data
    try:
        company_category = driver.find_element(By.XPATH,
                                               '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/\
            div/div[1]/div[2]/div/div[2]/span/span/button')

        company_category = company_category.text
    except NoSuchElementException:
        company_category = 'NA'

    try:
        rating = driver.find_element(By.XPATH,
                                     '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/\
            div/div[1]/div[2]/div/div[1]/div[2]/span[1]/span[1]')
        rating = rating.text
    except NoSuchElementException:
        rating = 'NA'
    except Exception as e:
        with open("../logs.txt", "a") as f:
            f.write(e)
            # traceback.TracebackException.from_exception(e).print(file=f)

    try:
        work_hours = driver.find_element(By.CLASS_NAME, 'o0Svhf').text
    except NoSuchElementException:
        work_hours = 'NA'

    final_url = driver.current_url

    try:
        wait = WebDriverWait(driver, 60)
        common_elements = wait.until(EC.visibility_of_any_elements_located(
            (By.CSS_SELECTOR, '.CsEnBe')))
        # elements = driver.find_elements(By.CSS_SELECTOR, '.CsEnBe')

        for element in common_elements:
            driver.execute_script("arguments[0].scrollIntoView(true);",
                                  element)
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
                    plus_code = value

        with open('file.csv', "a", encoding="utf-8") as fi:
            fi.write(
                f'"{title}",{company_category},{rating},{work_hours},"{address}",{website},{phone},"{plus_code}","{final_url}","{sent_keyword}"\n')
        print(f"Exported {title} ")
    except Exception as e:
        with open("../logs.txt", "a") as f:
            f.write(e)
            # traceback.TracebackException.from_exception(e).print(file=f)
        pass


def multiple_results(driver):
    "extracts links from page src, and then scrapes information"
    new_text = driver.page_source
    pattern = r'https://www\.google\.com\/maps\/place\/[^"]*'
    matches = re.findall(pattern, new_text)

    new_match = []
    for match in matches:  # iterates through the links
        new_match.append(match)
    # print(new_match)
    for link in new_match:
        driver.execute_script("window.open('about:blank', '_blank');")
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(1)
        driver.get(link)
        time.sleep(1)
        extract_information(driver)
    for handle in driver.window_handles[1:]:
        # once operation is done, closes all tabs except one
        driver.switch_to.window(handle)
        time.sleep(1)
        driver.close()
        time.sleep(1)
    driver.switch_to.window(driver.window_handles[0])


options = Options()
user_agent = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
              '(KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.37")')

# ua = UserAgent()
# user_agent = ua.random
# print(user_agent)
options.add_argument(f'--user-agent={user_agent}')
options.add_argument('--headless')
options.add_experimental_option("detach", True)
options.add_argument('--start-maximized')
options.add_argument("--disable-gpu")
try:
    # PROXY = '198.46.223.139:6246'
    # PROXY = requests.get("https://ipv4.webshare.io/",
    #              proxies={
    #         "http": "http://xrrmhvbs-rotate:nxagk0sfe561@p.webshare.io:80/",
    #         "https": "http://xrrmhvbs-rotate:nxagk0sfe561@p.webshare.io:80/"
    #              }).text
    #     print(PROXY)
    #     options.add_argument('--proxy-server=%s' % PROXY)

    s = Service(CHROMEDRIVER_PATH)

    driver = webdriver.Chrome(service=s, options=options)
    driver.get(MAPS_LINK)
except Exception as e:
    with open("../logs.txt", "a") as f:
        f.write(e)
        # traceback.TracebackException.from_exception(e).print(file=f)


def css_checker(driver):
    """
    checks if css selector '.CsEnBe' is present
    """
    try:
        driver.find_element(By.CSS_SELECTOR, '.CsEnBe')
        return True
    except NoSuchElementException:
        return False


def checking_url(driver):
    skipping_dir = 'https://www.google.com/maps/dir/'
    missing_url = driver.current_url
    if skipping_dir in missing_url:
        print('skipping...')
        page_src = driver.page_source
        with open(f'C:\\Users\\Kipplouser1\\Desktop\\1409_final\\page_src\\{title}.html', 'w', encoding='UTF-8') as f:
            f.writelines(page_src)

    driver.get(MAPS_LINK)


def main_scrape(keyword):
    global sent_keyword, search_box
    checking_url(driver)
    # finds the maps page, search box and button
    try:
        search_box = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="searchboxinput"]')))
    except selenium.common.exceptions.TimeoutException:
        with open("../logs.txt", "a") as f:
            f.write('Search box was not found! (Exception)\n')
        pass
    
    if search_box:
        print('Search box found!!')
    else:
        print("SearchBox not found!")
        with open("../logs.txt", "a") as fi:
            fi.write('Search Box not found! in line 230')
        pass
    time.sleep(1)
    search_box.click()
    time.sleep(1)
    search_box.send_keys(keyword)
    time.sleep(1)
    sent_keyword = keyword
    search_button = driver.find_element(By.XPATH,
                                        '//*[@id="searchbox-searchbutton"]')
    search_button.click()
    time.sleep(2)
    get_url = driver.current_url
    print("The current url is:" + str(get_url))

    matching_url = 'https://www.google.com/maps/place/'

    # skipping_dir = 'https://www.google.com/maps/dir/'
    # missing_url = driver.current_url
    # if skipping_dir in missing_url:
    #     print('skipping...')
    #     page_src = driver.page_source
    #     with open(f'C:\\Users\\Kipplouser1\\Desktop\\1409_final\\page_src\\{title}.html', 'w', encoding='UTF-8') as f:
    #         f.writelines(page_src)

    # driver.refresh()

    if matching_url in get_url:
        extract_information(driver)
    else:
        multiple_results(driver)
        try:
            search_box = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="searchboxinput"]')))
        except:
            driver.get(MAPS_LINK)
            time.sleep(1)
            pass
        if not search_box:
            driver.get(MAPS_LINK)
            time.sleep(1)
            pass
        else:
            search_box.clear()


if __name__ == "__main__":
    print("-------------------------------------------")
    print("""         Google Maps Scraper     """)
    print("-------------------------------------------")

    name_of_file = input("Enter the name of the csv file in the io folder: ")
    current_directory = os.getcwd()
    io_folder = 'io_folder'
    os.chdir(io_folder)
    new_directory = os.getcwd()
    print(f'You are currently in the right path: {new_directory}')
 
    print("Please wait...")
  
    os.system('cls')

    df = pd.read_csv(name_of_file)
    print('Processing the file....')

    df1 = df.iloc[:, 0]
    keywords = df1.to_list()
    keyword_length = len(keywords)
    # print(f'These are the keywords: {keywords}')
    print(f"Read all the {keyword_length} keywords in the csv file...")
  
    print("The result will be saved in --> 'file.csv' in the io_folder")


    print("The Scraping starting in..")
    for number in range(3, 0, -1):
        print(number)
        time.sleep(1)

    os.system('cls')

    num_processes = 15
    pool = multiprocessing.Pool(num_processes)
    try:
        # # applying function to each keyword
        pool.map(main_scrape, keywords)
    except Exception as e:
        with open("../logs.txt", "a") as f:
            f.write(str(e))
    # Close the pool
    pool.close()
    pool.join()
