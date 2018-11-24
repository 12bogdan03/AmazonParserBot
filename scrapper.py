import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from config import logger, BASEDIR


class Scrapper:
    def __init__(self):
        # chrome_options = Options()
        # chrome_options.add_argument("--headless")
        caps = DesiredCapabilities.PHANTOMJS
        caps["phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 ' \
                                                    '(KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        self.driver = webdriver.PhantomJS(os.path.join(BASEDIR,
                                                       'drivers',
                                                       'phantomjs'),
                                          desired_capabilities=caps)

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
