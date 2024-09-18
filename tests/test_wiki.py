import pytest
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


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
    wiki_search = driver.find_element(By.ID, "searchInput")
    wiki_search.click()
    wiki_search.clear()
    wiki_search.send_keys('колобок')
    wiki_search.submit()

    WebDriverWait(driver, 10).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete")

    search_link = driver.find_element(By.CSS_SELECTOR, 'div#mw-content-text > div > p:nth-of-type(11) > a')
    search_link.click()

    WebDriverWait(driver, 10).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete")

    title_word = driver.find_element(By.XPATH, '//*[@class="mw-page-title-main"]')
    text_title = driver.execute_script("return arguments[0].textContent", title_word)

    assert 'журнал' in text_title

    driver.quit()
