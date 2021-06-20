from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from colorama import Fore, Style, init
from selenium import webdriver
from datetime import datetime
from bots import messenger as msg
import logging
from requests.packages.urllib3.util.retry import Retry
from selenium.common.exceptions import TimeoutException
from requests.adapters import HTTPAdapter
import requests
from dotenv import load_dotenv
from time import sleep
from tqdm import tqdm
from bots.browser import Browser 
from bots.printer import Printer 
from bots.purchase import Purchase 
import requests
import random
import time
import re
import os
import re
from selenium.webdriver.support.wait import WebDriverWait


DEFAULT_HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
    "origin": "https://www.newegg.com",
}

AMAZON_URLS = {
    "BASE_URL": "https://{domain}/",
    "ALT_OFFER_URL": "https://{domain}/gp/offer-listing/",
    "OFFER_URL": "https://{domain}/dp/",
    "CART_URL": "https://{domain}/gp/cart/view.html",
    "ATC_URL": "https://{domain}/gp/aws/cart/add.html",
}

MAX_TIMEOUT = 10

class Amazon():

    def __init__(self, number, url, settings):

        load_dotenv()
        init(convert=True)
        self.logger = logging.getLogger()
        fhandler = logging.FileHandler(filename='.\\amazonLog.log', mode='a')
        self.logger.addHandler(fhandler)
        self.logger.setLevel(logging.INFO)
        #self.session = requests.Session()
        self.is_logged_in = False
        self.printer = Printer()
        self.az_base = "smile.amazon.com"
        if settings is not None:
            self.MAX_TIMEOUT = self.settings.max_timeout
        else:
            self.MAX_TIMEOUT = MAX_TIMEOUT

        # General settings
        self.settings = settings
        self.url = url
        self.stream_mode = settings.stream_mode
        self.instock_only_mode = settings.instock_only_mode

        # //*[@id="search"]/div[1]/div/div[1]/div/span[3]/div[2]/div[1]/div/span/div
        
        # What we're looking for
        self.cards_to_find = settings.cards_to_find
        self.card_prices = settings.card_prices

        # Login time
        self.login_at_start = settings.login_at_start

        # NewEgg settings
        self.az_info = settings.az_info

        self.number = number
        self.sku_id = sku_id = None

        # Browser driver
        self.browser = Browser(settings)
        self.driver = self.browser.driver
        self.driver.get(url)

        # Statistics
        self.avg_prices = self.total_prices = self.card_count = self.old_prices = {
            "3060" : 0,
            "3060 Ti" : 0,
            "3070" : 0,
            "3080" : 0,
            "3080 Ti" : 0,
            "3090" : 0
        }
        


        #adapter = HTTPAdapter(
        #    max_retries=Retry(
        #        total=3,
        #        backoff_factor=1,
        #        status_forcelist=[429, 500, 502, 503, 504],
        #        method_whitelist=["HEAD", "GET", "OPTIONS", "POST"],
        #    )
        #)
        #self.session.mount("https://", adapter)
        #self.session.mount("http://", adapter)
        #self.session.get(self.url)

        #response = self.session.get(
            #NEWEGG_PDP_URL.format(sku=self.sku_id), headers=DEFAULT_HEADERS
        #)

    def close_popup(self, path):
        """ Close popup window """

        self.driver.find_element_by_xpath(path).click()

    def get_chunks(self, desc):
        """ Break down description to extract only the first part. """

        chunks, chunk_size = len(desc), len(desc)//4
        pts = [desc[i:i+chunk_size] for i in range(0, chunks, chunk_size)]
        return pts[0]
    
    def get_timeout(self, timeout=MAX_TIMEOUT):
        return time.time() + timeout

    def login(self):
        timeout = self.get_timeout()
        while True:
            try:
                email_field = self.driver.find_element_by_xpath('//*[@id="ap_email"]')
                break
            except NoSuchElementException:
                try:
                    password_field = self.driver.find_element_by_xpath(
                        '//*[@id="ap_password"]'
                    )
                    break
                except NoSuchElementException:
                    pass
            if time.time() > timeout:
                break

    def get_card(self, item, description, ctype, is_in, link, display_desc, true_price):
        """ Sift through a list item and extrace card data. """

        # Get sold out tag if it exists
        try:
            sold_out = item.find_element_by_class_name("a-price-whole")
            sold_out = sold_out.text
        except NoSuchElementException:
            sold_out = "possibly"

        sku = link.split("=")[-1]
        if sold_out == '' or sold_out == None or sold_out == "possibly":
            in_stock = False
            self.printer.output(ctype, "OUT", "xxx", display_desc, "", self.stream_mode, "Newegg")
        else:
            in_stock = True
            print_desc = description.text[:20]
            if self.cards_to_find[ctype] is not None:
                if self.cards_to_find[ctype] and self.card_prices[ctype] > true_price:
                    self.printer.output(ctype, "IN", true_price,
                            print_desc, link, self.stream_mode, "NewEgg")
                    buy = Purchase(self.driver, item, sku, "newegg")
                    buy.make_purchase()
            else:
                self.printer.output(ctype, "EXP", true_price,
                        print_desc, link, self.stream_mode, "NewEgg")

    def select_dropdown(self):
        drop = self.driver.find_elements_by_class_name("form-select")
        drop[1].find_element(
            By.XPATH, "//*[@value='96']/option[text()='96']").click
        print(drop[1].find_element(
            By.XPATH, "//*[@value='96']/option[text()='96']"))

    def loop_body(self, item):
        if item.text == '':
            return
        description = item.find_element_by_class_name("""//*[@id="search"]/div[1]/div/div[1]/div/span[3]/div[2]/div[6]/div/span/div/div/div[2]/div[2]/div/div[1]/h2/a/span""")
        offer_xpath = (
                    "//div[@id='aod-offer' and .//input[@name='submit.addToCart']] | "
                    "//div[@id='aod-pinned-offer' and .//input[@name='submit.addToCart']]"
                )
        # Get sold out tag if it exists
        try:
            sold_out = item.find_element_by_class_name("item-promo")
            sold_out = sold_out.text

        except NoSuchElementException:
            sold_out = "possibly"

        if description.text == '':
            if self.settings.save_logs:
                self.logger.info("Error, no description text for item {}".format(item))
            return
        display_desc = self.get_chunks(description.text)
        is_in = True
        price = item.find_element_by_class_name("price-current")
        link = description.get_attribute("href")

        if "OUT" in sold_out or price.text == '':
            in_stock = False
        else:
            is_in = True
        true_price = float(
            re.sub(r'[^\d.]+', '', price.text.split('$')[1].strip()))

        for key in self.cards_to_find:
            if key in description.text:
                self.card_count[key] += 1
                self.total_prices[key] += 1
                self.avg_prices[key] = self.total_prices[key] / self.card_count[key]
                self.get_card(item, description, key, is_in, link, display_desc, true_price)
                break
        time.sleep(random.uniform(0, 1))


    def validate_body(self, count, dt_string):
        if "" in self.driver.title:
            #notice = self.driver.find_elements_by_class_name(
            #    "item-info")
            #stock = self.driver.find_elements_by_class_name(  # s-result-item
            #    "rush-component s-latency-cf-section")

            stock = self.driver.find_elements_by_class_name(  # s-result-item
                "s-result-item")

            #queue = []
            #queue = asyncio.Queue()

            #if not self.stream_mode:
            #        if self.settings.show_progress_bar:
            #            producers = [asyncio.create_task(self.loop_body(item)) for item in stock]
            #        else:
            #            producers = [asyncio.create_task(self.loop_body(item)) for item in stock]
            #else:
            #    if self.settings.show_price_line:
            #        self.printer.print_refresh(count, dt_string, self.old_prices, self.avg_prices)
            #    producers = [asyncio.create_task(self.loop_body(item)) for item in stock]

            #await asyncio.gather(*producers)
            #await queue.join()

            if not self.stream_mode:
                if self.settings.show_progress_bar:
                    for item in tqdm(stock):
                        self.loop_body(item)
                else:
                    for item in stock:
                        self.loop_body(item)
            else:
                for item in stock:
                    self.loop_body(item)
                self.printer.print_refresh(count, dt_string, self.old_prices, self.avg_prices)

            sleep_interval = 5+random.randrange(0, 1)
        elif self.driver.find_element_by_class_name("popup-close") != None:
            self.driver.find_element_by_class_name(
                "popup-close").click()

    def start(self):

        self.driver.get(self.url)
        count = 1
        try:
            while True:
                t0 = time.time()
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

                delay = 3 # seconds
                try:
                    myElem = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'newegg-feedback')))
                    print("Page is ready!")
                except TimeoutException:
                    print("Loading took too much time!")

                # Update prices
                for key in self.old_prices:
                    self.old_prices[key] = self.avg_prices[key]
                t0 = time.time()
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                if self.settings.save_logs:
                    msg = ""
                    for key in self.avg_prices:
                        msg += key + ': $' + str(self.avg_prices[key]) + ', '
                    msg += 'Iterations: ' + str(count)
                    self.logger.info(msg)

                self.validate_body(count, dt_string)

                count += 1
                t1 = time.time()
                diff = t1 - t0
                print("diff: ", diff)
                if count % 3 == 0 and diff < 3:
                    break
                self.driver.refresh()
        except KeyboardInterrupt:
            pass
