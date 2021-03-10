
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

from selenium import webdriver

import random
import re
from colorama import Fore, Style, init
import os
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import requests
import re
#from utils.logger import log
from . import secret_messenger as msg
#import bot.messenger as msg
from datetime import datetime
from time import sleep
from tqdm import tqdm
import logging
from dotenv import load_dotenv


BEST_BUY_PDP_URL = "https://api.bestbuy.com/click/5592e2b895800000/{sku}/pdp"
BEST_BUY_CART_URL = "https://api.bestbuy.com/click/5592e2b895800000/{sku}/cart"

BEST_BUY_ADD_TO_CART_API_URL = "https://www.bestbuy.com/cart/api/v1/addToCart"
BEST_BUY_CHECKOUT_URL = "https://www.bestbuy.com/checkout/c/orders/{order_id}/"

DEFAULT_HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
    "origin": "https://www.bestbuy.com",
}

options = Options()
options.page_load_strategy = "eager"
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)
options.add_argument("user-data-dir=.profile-bb")
options.add_argument("user-data-dir=/home/kms/.config/google-chrome/Defaule")

class BestBuy():

    def __init__(self, number, mode, signin_mode, url, sku_id=6429440, headless=False):

        load_dotenv()
        init(convert=True)
        self.logger = logging.getLogger()
        fhandler = logging.FileHandler(filename='.\\bestBuyLog.log', mode='a')
        self.logger.addHandler(fhandler)
        self.logger.setLevel(logging.INFO)
        self.session = requests.Session()

        self.url = url
        self.mode = mode
        self.number = number
        self.sku_id = sku_id
        self.signin_with_google = signin_mode

        self.bestbuy_password = os.environ.get("bestbuy_password")
        self.bestbuy_email = os.environ.get("bestbuy_email")
        #options.binary_location(executable_path=r'/mnt/d/New-Chrome-Driver/chromedriver.exe')
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)

        adapter = HTTPAdapter(
            max_retries=Retry(
                total=3,
                backoff_factor=1,
                status_forcelist=[429, 500, 502, 503, 504],
                method_whitelist=["HEAD", "GET", "OPTIONS", "POST"],
            )
        )
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        self.session.get(self.url)

        response = self.session.get(
            BEST_BUY_PDP_URL.format(sku=self.sku_id), headers=DEFAULT_HEADERS
        )

    def login(self):
        if "Account" not in self.driver.find_element_by_xpath("//*[@id=\"header-block\"]/div[2]/div[2]/div/nav[2]/ul/li[1]/button/div[2]/span").text:
            return
        if self.signin_with_google:
            self.driver.get("https://www.bestbuy.com/identity/global/signin")
            self.driver.find_element_by_xpath(
                '/html/body/div[1]/div/section/main/div[1]/div/div/div[2]/div/div[3]/button')
            '/html/body/div[1]/div/section/main/div[1]/div/div/div/div/div[3]/button'
            self.driver.find_element_by_xpath(
                '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div/div/ul/li[3]/div/div[1]/div/div[2]').click()
        else:
            
            self.driver.get("https://www.bestbuy.com/identity/global/signin")
            self.driver.find_element_by_xpath('//*[@id="fld-e"]').send_keys(
                self.bestbuy_email
            )
            self.driver.find_element_by_xpath('//*[@id="fld-p1"]').send_keys(
                self.bestbuy_password
            )
            self.driver.find_element_by_xpath("//*[contains(text(), 'Sign In')]").click()
            # /html/body/div[1]/div/section/main/div[1]/div/div/div/div/form/div[3]/button

            #self.driver.find_element_by_xpath(
                # "/html/body/div[1]/div/section/main/div[1]/div/div/div/div/form/div[3]/button"
            #    "/html/body/div[1]/div/section/main/div[1]/div/div/div/div/form/div[4]/button"
            #).click()
            # self.driver.find_element_by_xpath(
            #    "/html/body/div[1]/div/section/main/div[1]/div/div/div/div/form/div[4]/button"
            # ).click()
        WebDriverWait(self.driver, 10).until(
            lambda x: "Official Online Store" in self.driver.title
        )

    def output(self, ctype, success, price, details, link):

        platform = "BestBuy"
        if success == "IN":
            print(Fore.GREEN + success, end==" ")
            print(" STOCK! | ${}  | {} | {} | {}".format(
                price, ctype, platform, details[0], link))
            if ctype == "3080":
                msg.send_message(self.number, link)
        elif self.mode is '1':
            if success == "EXP":
                print(Fore.YELLOW + success, end==" ")
                print(" | ${}  | {} | {} | {}".format(
                    price, ctype, platform, details[0]))
            elif success == "OUT":
                print(Fore.RED + success, end==" ")
                print("OF STOCK | ${}  | {} | {} | {}".format(
                    price, ctype, platform, details[0]))
            else:
                print("No data found")
        Style.RESET_ALL

    def get_chunks(self, desc):
        new_desc = desc.split("\n")[0]
        return new_desc

    def get_card(self, item, description, ctype, is_in, link):

        if not is_in or "Sold Out" in description.split("\n"):
            in_stock = False
            self.output(ctype, "OUT", "xxx", description.split("\n"), "link")
        else:
            in_stock = True
            true_price = float(
                re.sub(r'[^\d.]+', '', description.split('$')[1].strip()))
            if ctype == "3080" and true_price < 1000:
                self.output(ctype, "IN", true_price,
                            description.split("\n"), link)
            elif ctype == "3090" and true_price < 1900:
                self.output(ctype, "IN", true_price,
                            description.split("\n"), link)
            elif ctype == "3060" and true_price < 600:
                self.output(ctype, "IN", true_price,
                            description.split("\n"), link)
            else:
                self.output(ctype, "EXP", true_price,
                            description.split("\n"), link)

    def check_country_page(self):
        try:
            if "Select your Country" in self.driver.title:
                self.driver.find_element_by_xpath(
                    '/html/body/div[2]/div/div/div/div[1]/div[2]/a[2]').click()
                # driver.find_element_by_class_name("us-link").click()
        except NoSuchElementException:
            print("no block")

    def check_popup(self, driver):
        try:
            if self.driver.find_element_by_id("survey_invite_no"):
                self.driver.find_element_by_id("survey_invite_no").click()
        except NoSuchElementException:
            print("no block")

    # Pass xpath of popup close button

    def close_popup(self, driver, path):

        self.driver.find_element_by_xpath(path).click()

    def close_deals_popup(self):
        try:
            if self.driver.find_element_by_xpath("//*[@id=\"widgets-view-email-modal-mount\"]/div/div/div[1]/div/div/div/div/button"):
                self.driver.find_element_by_xpath(
                    "//*[@id=\"widgets-view-email-modal-mount\"]/div/div/div[1]/div/div/div/div/button").click()
        except NoSuchElementException:
            print("no popup")

    def loop_body(self, item):
        description = item.text
        link_item = item.find_element_by_class_name("sku-header")
        link = item.find_element_by_tag_name("a").get_attribute("href")

        parts = description.split("\n")
        cart_button = item.find_element_by_class_name("c-reviews-v4 ")
        nope = False
        if "Not yet reviewed" in cart_button.text:
            nope = True

        # print(parts[0], "\n", parts[1], "\n", parts[2], "\n", parts[4], "\n", parts[5], "\n")

        if len(parts) < 3 or "Sold Out" in parts[3] or nope:
            is_in = False
        else:
            is_in = True

        if "3080" in parts[0]:
            self.get_card(item, description, "3080", is_in, link)
        elif "3080" in parts[0]:
            self.get_card(item, description, "3060", is_in, link)
        elif "3090" in parts[0]:
            pass
            # self.get_card(item, description, "3090", is_in, link)
        time.sleep(random.uniform(0, 1))

    def start(self):

        count = 1
        try:
            self.check_country_page()
            self.login()
            self.close_deals_popup()
            while True:
                try:
                    t0 = time.time()
                    now = datetime.now()
                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                    # self.logger.info("Line 146, Refresh: " + str(count))

                    print('\n<=======================BestBuy Refresh #:{}, {}=======================>'.format(
                        count, dt_string))

                    if "GPUs" in self.driver.title:
                        notice = self.driver.find_elements_by_class_name(
                            "item-info")
                        total = self.driver.find_element_by_id("main-results")
                        stock = total.find_elements_by_class_name("sku-item")
                        is80 = False
                        is90 = False

                        # print(description.split("\n")[0]) # Description
                        # print(description.split("\n")[2]) # rating
                        # print(description.split("\n")[4]) # Sold Out
                        # print(description.split("\n")[8]) # price

                        if self.mode == '2':
                            for item in tqdm(stock):
                                self.loop_body(item)
                        else:
                            for item in stock:
                                self.loop_body(item)

                        sleep_interval = 5+random.randrange(0, 1)

                    count += 1
                    t1 = time.time()
                    diff = t1 - t0
                    print("diff: ", diff)
                    if count % 3 == 0 and diff < 3:
                        break
                    self.driver.refresh()
                except NoSuchElementException:
                    self.logger.error(
                        "Unable to find element. Refresh: " + str(count))
        except KeyboardInterrupt:
            self.driver.quit()
            pass


# line 413, in find_elements_by_class_name
#     return self.find_elements(by=By.CLASS_NAME, value=name)
#   File "C:\Users\Kyle\AppData\Roaming\Python\Python37\site-packages\selenium\webdriver\remote\webelement.py", line 685, in find_elements
#     {"using": by, "value": value})['value']
#   File "C:\Users\Kyle\AppData\Roaming\Python\Python37\site-packages\selenium\webdriver\remote\webelement.py", line 633, in _execute
#     return self._parent.execute(command, params)
#   File "C:\Users\Kyle\AppData\Roaming\Python\Python37\site-packages\selenium\webdriver\remote\webdriver.py", line 321, in execute
#     self.error_handler.check_response(response)
#   File "C:\Users\Kyle\AppData\Roaming\Python\Python37\site-packages\selenium\webdriver\remote\errorhandler.py", line 242, in check_response
#     raise exception_class(message, screen, stacktrace)
# selenium.common.exceptions.WebDriverException: Message: out of memory
