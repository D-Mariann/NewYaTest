import time
import chromedriver_autoinstaller
import pytest
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from pages.the_search_phrase import *
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, InvalidSelectorException




@pytest.fixture
def driver():
    chromedriver_autoinstaller.install()
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=Service(), options=options)
    return driver



def test_search_wiki(driver):

    driver.get("https://ru.wikipedia.org/")
    wiki_search = driver.find_element(By.ID ,"searchInput")
    wiki_search.click()
    wiki_search.clear()
    wiki_search.send_keys('колобок')
    wiki_search.submit()

    WebDriverWait(driver, 10).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete")

    search_link = driver.find_element(By.XPATH, '//*[@id="mw-content-text"]//a[1]')
    search_link.click()

    WebDriverWait(driver, 10).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete")


    assert 'журнал' in driver.title
    # # title_word = driver.find_element(By.XPATH,'//*[@class="mw-page-title-main"and contains(text(), "журнал")]')
    # title_word = driver.find_element(By.XPATH, '//*[@class="mw-page-title-main"]')
    # text_title = driver.execute_script("return arguments[0].textContent",title_word)
    # # title_word.get_attribute('textContent'))
    # print(text_title)
    # print(ti)
    driver.quit()