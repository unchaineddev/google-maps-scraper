import re
import time
# import traceback

# import requests
import psycopg2
from psycopg2 import pool
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# from initialize_database import postgres_db
from checker import css_checker, checking_url

CHROMEDRIVER_PATH = r'C:\Users\Kipplouser1\Desktop\maps\chromedriver.exe'
PAGE_SRC_PATH = r'C:\Users\Kipplouser1\Desktop\maps\page_src'
MAPS_LINK = 'https://www.google.com/maps'
timeout = 60
print('Starting Scraper')

# initializing options for the driver 
options = Options()
user_agent = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
              '(KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.37")')
options.add_argument(f'--user-agent={user_agent}')
options.add_argument('--headless')
options.add_experimental_option("detach", True)
options.add_argument('--start-maximized')
options.add_argument("--disable-gpu")

# Connecting to Database and creating a pool of connections
postgreSQL_pool = psycopg2.pool.ThreadedConnectionPool(15,
                                                       27,
                                                       user="postgres",
                                                       password="123456789",
                                                       host="localhost",
                                                       port="5432",
                                                       database="google",
                                                       connect_timeout=3,
                                                       keepalives=1,
                                                       keepalives_idle=5,
                                                       keepalives_interval=2,
                                                       keepalives_count=2)

if postgreSQL_pool:
    print("Connection pool created successfully")
try:
    # # Proxy Code
    # PROXY = requests.get("https://ipv4.webshare.io/",
    #              proxies={
    #         "http": "http://example:example@host:port/",
    #         "https": "http://example:example@host:port/"
    #              }).text
    #     print(PROXY)
    #     options.add_argument('--proxy-server=%s' % PROXY)

    s = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=s, options=options)
    driver.get(MAPS_LINK)
except Exception as e:
    with open("logs.txt", "a") as f:
        f.write(str(e))
        # traceback.TracebackException.from_exception(e).print(file=f)


def extract_information(driver):
    """extract all information in the page"""
    global title, rating, website, phone, plus_code, address

    # checks if css of the actual company page present
    if not css_checker(driver):
        return
    else:
        print("CSS found for the page..extracting info!!")

    try:
        # Searching for the title
        title = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/\
                    div[1]/div/div/div[2]/div/div[1]/div[1]/h1')))
        title = title.text
        print(f'Found "{title}"... extracting the rest of the data')

        # If the title is not found, and the url is incorrect, saves page src
    except selenium.common.exceptions.TimeoutException:
        print('Could not find the title!')
        skipping_dir = 'https://www.google.com/maps/dir/'
        missing_url = driver.current_url
        if skipping_dir in missing_url:
            print('skipping...')
            page_src = driver.page_source
            with open(rf'{PAGE_SRC_PATH}\{title}.html', 'w', encoding='UTF-8') as f:
                f.writelines(page_src)
            driver.refresh()

    # if company title is found, scrapes rest of the data
    try:
        company_category = driver.find_element(
            By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/\
                div/div/div[2]/div/div[1]/div[2]/div/div[2]/span/span/button')

        company_category = company_category.text
    except NoSuchElementException:
        company_category = 'NA'

    try:
        rating = driver.find_element(
            By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/\
                div/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/span[1]/span[1]')
        rating = rating.text
    except NoSuchElementException:
        rating = 'NA'
    except Exception as e:
        with open("logs.txt", "a") as f:
            f.write(str(e))
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

        # Google Maps have some fields with a common class name
        # this loop iterates through the elements and extracts the accurate results
        driver.implicitly_wait(1)
        for element in common_elements:
            driver.execute_script("arguments[0].scrollIntoView(true);",
                                  element)
            aria_label = element.get_attribute("aria-label")
            # print(aria_label)

            pattern = r'(\w+): ([^\n]+)'
            matches = re.findall(pattern, aria_label)
            key_value_pairs = dict(matches)
            # print(key_value_pairs)

            # extracts ---> address, website, phone number and plus code
            for key, value in key_value_pairs.items():
                if key == 'Address':
                    address = value
                if key == 'Website':
                    website = value
                if key == 'Phone':
                    phone = value
                if key == 'code':
                    plus_code = value


        # saves the result in a csv file
        # with open('file.csv', "a", encoding="utf-8") as fi:
        #     fi.write(
        #         f'"{title}",{company_category},{rating},{work_hours},"{address}",{website},{phone},"{plus_code}","{final_url}","{sent_keyword}"\n')
        # print(f"Exported {title} ")


        # Export to DB
        connn = postgreSQL_pool.getconn()
        cur_object = connn.cursor()
        QUERY = """
           INSERT INTO MAPS 
           (comp_title, comp_category, comp_rating, comp_hours, 
           comp_address, comp_site, comp_phone, comp_pluscode, 
           comp_link, keyword_sent)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
           """

        values = (title, company_category, rating, work_hours, address,
                  website, phone, plus_code, final_url, sent_keyword)
        cur_object.execute(QUERY, values)
        # values_list = [(title, company_category, rating, work_hours, address,
        #         website, phone, plus_code, final_url, sent_keyword)]
        # cur_object.executemany(QUERY, values_list)

        connn.commit()
        cur_object.close()
        postgreSQL_pool.putconn(connn)
        print(f'{title} was exported to the DB')

    except Exception:
        pass


def multiple_results(driver):
    """extracts links from page src, and then scrapes information;
    this function is called when the /place endpoint is not found.
    """
    new_text = driver.page_source
    pattern = r'https://www\.google\.com\/maps\/place\/[^"]*'
    matches = re.findall(pattern, new_text)

    new_match = []
    for match in matches:  # iterates through the links
        new_match.append(match)
    # print(new_match)
    for link in new_match:
        # opens each page in a new about:blank page
        driver.execute_script("window.open('about:blank', '_blank');")
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[-1])  # switch the tab
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


def main_scrape(keyword):
    global sent_keyword, search_box
    checking_url(driver)
    # finds the maps page, search box and button
    try:
        search_box = WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="searchboxinput"]')))
    except selenium.common.exceptions.TimeoutException:
        with open("logs.txt", "a") as f:
            f.write('Searchbox was not found! (Exception)')
        pass

    if search_box:
        print('Searchbox found!!')
    else:
        print("SearchBox not found!")
        with open("logs.txt", "a") as f:
            f.write('Search Box not found! Trying again!')
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
    if matching_url in get_url:
        extract_information(driver)
    else:
        multiple_results(driver)
        try:
            search_box = WebDriverWait(driver, timeout).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="searchboxinput"]')))
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
