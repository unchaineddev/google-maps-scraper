# Global Constants
CHROMEDRIVER_PATH = r"C:\Users\Kipplouser1\Desktop\test\chromedriver.exe"
FILE_RAW = "all.csv"
CSV_FILE_PATH = "file.csv"
COMMON_XPATH = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/'


import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC


# prox = Proxy()
# prox.proxy_type = ProxyType.MANUAL
# prox.http_proxy = "ip_addr:port"
# prox.socks_proxy = "ip_addr:port"
# prox.ssl_proxy = "ip_addr:port"
# capabilities = webdriver.DesiredCapabilities.CHROME
# prox.add_to_capabilities(capabilities)


def maps_scraper():
    """reading file, extracting csv files and converting it to a list"""
    df = pd.read_csv(FILE_RAW)
    links = df['link'].to_list()

    # iterating through the list of URLs
    for link in links:
        count = 0
        # Load Browser with Chrome Options
        options = webdriver.ChromeOptions()
        service = ChromeService(executable_path=CHROMEDRIVER_PATH)
        # desired_capabilities=capabilities)
        # options.add_argument("--start-maximized")
        options.add_argument('--headless')
        driver = webdriver.Chrome(service=service, options=options)


        try:
            driver.get(link)

            # Extracting all data from page
            company_name = driver.find_element(By.CSS_SELECTOR, '.DUwDvf')

            company_category = driver.find_element(By.XPATH, COMMON_XPATH 
                + 'div[2]/div/div[1]/div[2]/div/div[2]/span/span/button')
            
            company_reviews = driver.find_element(By.XPATH, COMMON_XPATH 
                + 'div[2]/div/div[1]/div[2]/div/div[1]/div[2]/span[1]/span[1]') 
            
            company_addr = driver.find_element(By.XPATH, COMMON_XPATH 
                + 'div[7]/div[3]/button/div/div[2]/div[1]')
            
            company_phone = driver.find_element(By.XPATH, COMMON_XPATH 
                + 'div[7]/div[7]/button/div/div[2]/div[1]')
            
            company_hours = driver.find_element(By.CLASS_NAME, 'ZDu9vd')
            try:
                company_site = driver.find_element(By.CLASS_NAME, 'ITvuef')
                comp_site = company_site.get_attribute('innerText')
            except:
                comp_site = "Site Unavailable"
                # print(script)
        except:
            print('this had an error')
        
        
    

        compname = company_name.text
        category = company_category.text
        reviews = company_reviews.text 
        address = company_addr.text 
        phone = company_phone.text
        work_hours = company_hours.text
        site = comp_site

        print(phone)
        
        
        with open(CSV_FILE_PATH, "a",  encoding="utf-8") as fi:
            fi.write(f'"{compname}",{category},{reviews},"{site}","""{address}""","{work_hours}"\n')

            
maps_scraper()
