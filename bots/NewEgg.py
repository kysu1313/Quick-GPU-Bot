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
from bots.logger import Logger
import requests
import random
import time
import re
import os
import re
from selenium.webdriver.support.wait import WebDriverWait

NEWEGG_PDP_URL = "https://api.bestbuy.com/click/5592e2b895800000/{sku}/pdp"
NEWEGG_CART_URL = "https://api.bestbuy.com/click/5592e2b895800000/{sku}/cart"
NEWEGG_ADD_TO_CART = "https://secure.newegg.com/Shopping/AddToCart.aspx?Submit=ADD&ItemList={sku}"

DEFAULT_HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
    "origin": "https://www.newegg.com",
}

class NewEgg():

    def __init__(self, number, url, settings, debug):

        load_dotenv()
        init(convert=True)
        fhandler = logging.FileHandler(filename='.\\neweggLog.log', mode='a')
        self.logger = Logger(fhandler)
        self.session = requests.Session()
        self.is_logged_in = False
        self.debug = debug
        self.printer = Printer()

        # General settings
        self.settings = settings
        self.url = url
        self.stream_mode = settings.stream_mode
        self.instock_only_mode = settings.instock_only_mode
        
        # What we're looking for
        self.cards_to_find = settings.cards_to_find
        self.card_prices = settings.card_prices

        # Login time
        self.login_at_start = settings.login_at_start

        # Statistics
        self.avg_prices = self.total_prices = self.card_count = self.old_prices = {
            "3060" : 0,
            "3060 Ti" : 0,
            "3070" : 0,
            "3080" : 0,
            "3080 Ti" : 0,
            "3090" : 0
        }
        
        # NewEgg settings
        self.ne_info = settings.ne_info

        self.number = number
        self.sku_id = sku_id = None

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
            NEWEGG_PDP_URL.format(sku=self.sku_id), headers=DEFAULT_HEADERS
        )

        # Browser driver
        self.browser = Browser(settings)
        self.driver = self.browser.driver
        self.driver.get(url)

    def close_popup(self, path):
        """ Close popup window """

        self.driver.find_element_by_xpath(path).click()

    def login(self):
        try:
            if self.find_element_by_class_name('nav-complex-title').text == "Sign in / Register":
                self.driver.find_element_by_xpath("//*[contains(text(), 'Sign in / Register')]").click()
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "signin-title"))
                )
                self.driver.find_element_by_id("labeled-input-signEmail").send_keys(self.settings.ne_info['ne_email'])
                self.driver.find_element_by_id("signInSubmit").click()
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "labeled-input-password"))
                )
                self.driver.find_element_by_id("labeled-input-password").send_keys(self.settings.ne_info['ne_password'])
                self.driver.find_element_by_id("signInSubmit").click()
        except Exception as e:
            if self.settings.save_logs:
                self.logger.log_info("Error in get_card: {}".format(e))
            pass
        self.is_logged_in = True

    def get_chunks(self, desc):
        """ Break down description to extract only the first part. """

        chunks, chunk_size = len(desc), len(desc)//4
        pts = [desc[i:i+chunk_size] for i in range(0, chunks, chunk_size)]
        return pts[0]

    def get_card(self, item, description, ctype, is_in, link, display_desc, true_price):
        """ Sift through a list item and extrace card data. """
        try:
            # Get sold out tag if it exists
            try:
                sold_out = item.find_element_by_class_name("item-promo")
                sold_out = sold_out.text
            except NoSuchElementException:
                sold_out = "possibly"

            sku = link.split("=")[-1]
            if sold_out == 'OUT OF STOCK':
                in_stock = False
                self.printer.output(ctype, "OUT", "xxx", display_desc, "", self.stream_mode, "Newegg")
            else:
                in_stock = True
                print_desc = description.text[:20]
                if self.cards_to_find[ctype] is not None:
                    if self.cards_to_find[ctype] and true_price < self.card_prices[ctype]:
                        self.printer.output(ctype, "IN", true_price,
                                print_desc, link, self.stream_mode, "NewEgg")
                        buy = Purchase(self.driver, item, 6426710, "newegg", self.is_logged_in, self.logger, self.settings)
                        buy.make_purchase_ne()
                else:
                    self.printer.output(ctype, "EXP", true_price,
                            print_desc, link, self.stream_mode, "NewEgg")
        except Exception as e:
            if self.settings.save_logs:
                self.logger.log_info("Error in get_card: {}".format(e))
            pass

    def select_dropdown(self):
        try:
            drop = self.driver.find_elements_by_class_name("form-select")
            drop[1].find_element(
                By.XPATH, "//*[@value='96']/option[text()='96']").click
            print(drop[1].find_element(
                By.XPATH, "//*[@value='96']/option[text()='96']"))
        except Exception as e:
            if self.settings.save_logs:
                self.logger.log_info("Error in select_dropdown: {}".format(e))
            pass

    def loop_body(self, item):
        try:
            if item.text == '':
                return
            WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "page-section"))
                )
            description = item.find_element_by_class_name("item-title")

            # Get sold out tag if it exists
            try:
                sold_out = item.find_element_by_class_name("item-promo")
                sold_out = sold_out.text

            except NoSuchElementException:
                sold_out = "possibly"

            if description.text == '':
                if self.settings.save_logs:
                    self.logger.log_info("Error, no description text for item {}".format(item))
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

            #if self.debug:
            #    buy = Purchase(self.driver, item, 6426710, "newegg", self.is_logged_in, self.logger, self.settings)
            #    buy.make_purchase_ne()

            for key in self.cards_to_find:
                if key in description.text:
                    self.card_count[key] += 1
                    self.total_prices[key] += 1
                    self.avg_prices[key] = self.total_prices[key] / self.card_count[key]
                    self.get_card(item, description, key, is_in, link, display_desc, true_price)
                    break
            time.sleep(random.uniform(0, 1))
        except Exception as e:
            if self.settings.save_logs:
                self.logger.log_info("Error in loop_body: {}".format(e))
            pass


    def validate_body(self, count, dt_string):
        try:
            if "" in self.driver.title:
                notice = self.driver.find_elements_by_class_name(
                    "item-info")
                stock = self.driver.find_elements_by_class_name(
                    "item-container")

                if not self.stream_mode:
                    if self.settings.show_progress_bar:
                        for item in tqdm(stock):
                            self.loop_body(item)
                    else:
                        for item in stock:
                            self.loop_body(item)
                else:
                    self.printer.print_refresh(count, dt_string, self.old_prices, self.avg_prices)
                    for item in stock:
                        self.loop_body(item)

                sleep_interval = 2+random.randrange(0, 1)
            elif self.driver.find_element_by_class_name("popup-close") != None:
                self.driver.find_element_by_class_name(
                    "popup-close").click()
        except Exception as e:
            if self.settings.save_logs:
                self.logger.log_info("Error in loop_body: {}".format(e))
            pass

    def start(self):

        self.driver.get(self.url)
        self.login()
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
                    self.logger.log_info(msg)

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
