import time
import chromedriver_autoinstaller
import pytest
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from pages.the_search_phrase import *
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException



@pytest.fixture
def driver():
    chromedriver_autoinstaller.install()
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=Service(), options=options)
    return driver



def test_search_yandex(driver):

    driver.get("https://www.ya.ru")
    yandex_search = driver.find_element(By.ID ,"text")
    yandex_search.click()
    yandex_search.clear()
    yandex_search.send_keys(the_search_phrase1)
    yandex_search.submit()


    time.sleep(3)
    driver.refresh()
    time.sleep(3)
    driver.refresh()


    WebDriverWait(driver, 10).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete")

    old_url = driver.current_url
    try:
        ya_element = driver.find_elements(By.XPATH,
                                          '//span[@class="ExtendedText-Short" and contains(text(), "песни для")]/../../../../../../div/div/a')
        
        for element in ya_element:
            element.click()

        # checking = WebDriverWait(driver, 20).until(lambda driver: old_url == driver.current_url)

        time.sleep(2)  # ставлю явное ожидание, потому что чаще всего открывается Ютуб, который не грузится до конца
        # и ожидание выше выдает ошибку TimeoutException
        driver.switch_to.window(driver.window_handles[1])
        checking = driver.current_url

        if checking == old_url:
            ya_element = driver.find_elements(By.XPATH,
                                              '//span[@class="OrganicTextContentSpan" and contains(text(), "песни для")]/../../../div/a')                            
            for element in ya_element:
                element.click()
                
            time.sleep(3)
            driver.switch_to.window(driver.window_handles[1])
            checking2 = driver.current_url
            # assert WebDriverWait(driver, 20).until(lambda driver: old_url != driver.current_url)
            assert checking2 != old_url
            print('the transition to the desired page is successful')
            
    except NoSuchElementException:
        print("exception handled, ebany yandex")

    else:   
        try:
            search_text = driver.find_elements(By.XPATH, f'//*[contains(text(), {search_for_matches})]') #это не найдет, провал
            # search_text = driver.find_elements(By.XPATH, '//*[contains(text(), "зимой")]')  #Это найдет и тест пройдет
            assert search_text
            print('the search is ok')
        except InvalidSelectorException:
            print(f'Search error, {substring_phrase} не найдено')
    driver.close()






