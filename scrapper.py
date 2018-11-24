import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from config import logger, BASEDIR


class Scrapper:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(os.path.join(BASEDIR,
                                                    'drivers',
                                                    'chromedriver'),
                                       chrome_options=chrome_options)

    def __del__(self):
        self.driver.close()

    def go_to(self, link):
        self.driver.get(link)

    def get_price(self):
        price = self.driver.find_element_by_id('priceblock_ourprice')
        return float(price.text.strip('$'))

    def get_title(self):
        title = self.driver.find_element_by_name('title')
        return title.get_attribute('content').split(' : ')[1]
