from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

MAPS_LINK = 'https://www.google.com/maps'
PAGE_SRC_PATH = r'C:\Users\Kipplouser1\Desktop\maps\page_src'


def css_checker(driver):
    """checks if css selector '.CsEnBe' is present"""
    try:
        driver.find_element(By.CSS_SELECTOR, '.CsEnBe')
        return True
    except NoSuchElementException:
        return False


def checking_url(driver):
    """if page redirects to the below url,this function is called to skip it"""
    global title
    skipping_dir = 'https://www.google.com/maps/dir/'
    missing_url = driver.current_url
    if skipping_dir in missing_url:
        print('skipping...')
        page_src = driver.page_source
        with open(rf'{PAGE_SRC_PATH}\{title}.html', 'w', encoding='UTF-8') as f:
            f.writelines(page_src)
    driver.get(MAPS_LINK)
