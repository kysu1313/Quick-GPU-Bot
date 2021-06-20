from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import random
import re
from colorama import Fore, Style, init
import os
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from concurrent.futures import ThreadPoolExecutor
from selenium.common.exceptions import TimeoutException, WebDriverException
#import multiprocessing as mp
import requests
#import resource
from . import messenger as msg
from datetime import date, datetime
from time import sleep
from tqdm import tqdm
import logging
from dotenv import load_dotenv
from bots.browser import Browser 
from bots.printer import Printer 
from bots.purchase import Purchase
from bots.logger import Logger
import sys
import asyncio
#from progress.bar import Spinner



BEST_BUY_PDP_URL = "https://api.bestbuy.com/click/5592e2b895800000/{sku}/pdp"
BEST_BUY_CART_URL = "https://api.bestbuy.com/click/5592e2b895800000/{sku}/cart"

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


class BestBuy():

    def __init__(self, number, url, settings, debug=False):

        load_dotenv()
        init(convert=True)

        fhandler = logging.FileHandler(filename='.\\bestBuyLog.log', mode='a')
        self.logger = Logger(fhandler)
        #self.session = requests.Session()
        self.is_logged_in = False
        self.printer = Printer()
        self.debug = debug

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
        self.avg_prices = self.total_prices = self.card_count = self.old_prices = {}
        for key in self.cards_to_find:
            self.avg_prices[key] = self.total_prices[key] = self.card_count[key] = self.old_prices[key] = 0
        
        # BestBuy settings
        self.bb_info = settings.bb_info

        self.number = number
        self.sku_id = ""
        self.item_count = 0
        self.total_time = 0

        # Browser driver
        self.browser = Browser(settings)
        self.driver = self.browser.driver
        self.driver.get(url)

    def login(self):
        if self.bb_info["bb_auto_login"]:
            try:
                if self.settings.DEBUG_MODE and not self.debug["login_enabled"]:
                    return
                if "Account" not in self.driver.find_element_by_class_name("account-button").text:
                    self.is_logged_in = True
                    return
                else:
                    self.driver.get("https://www.bestbuy.com/identity/global/signin")
                    WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="fld-p1"]')))
                    if self.driver.find_element_by_xpath('//*[@id="fld-p1"]').get_attribute("value") != None:
                        self.driver.find_element_by_xpath("/html/body/div[1]/div/section/main/div[2]/div[1]/div/div/div/div/form/div[4]/button").click()
                    else:
                        self.driver.find_element_by_xpath("//*[contains(text(), 'Sign')]").send_keys(
                            self.settings.bb_info["bb_email"]
                        )
                        self.driver.find_element_by_xpath('//*[@id="fld-p1"]').send_keys(
                            self.settings.bb_info["bb_password"]
                        )
                        self.driver.find_element_by_xpath("/html/body/div[1]/div/section/main/div[2]/div[1]/div/div/div/div/form/div[4]/button").click()
                WebDriverWait(self.driver, 6).until(
                    lambda x: "Official Online Store" in self.driver.title
                )
                self.is_logged_in = True
            except Exception as e:
                if self.settings.save_logs:
                    self.logger.log_info("Login Failure: {}".format(e))
                pass
            self.driver.get(self.url)

    def get_chunks(self, desc):
        new_desc = desc.split("\n")[0]
        return new_desc

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

    def close_feedback_popup(self):
        # Take the Survey
        try:
            if self.driver.find_element_by_id("survey_invite_no"):
                self.driver.find_element_by_id("survey_invite_no").click()
        except NoSuchElementException:
            print("No popup")


    def close_deals_popup(self):
        try:
            if self.driver.find_element_by_xpath("//*[@id=\"widgets-view-email-modal-mount\"]/div/div/div[1]/div/div/div/div/button"):
                self.driver.find_element_by_xpath(
                    "//*[@id=\"widgets-view-email-modal-mount\"]/div/div/div[1]/div/div/div/div/button").click()
        except NoSuchElementException:
            print("no popup")

    def get_card(self, item, description, ctype, true_price, is_in, link):
        #if self.debug:
        #    buy = Purchase(self.driver, item, 6426710, "bestbuy", self.is_logged_in, self.logger, self.settings)
        #    buy.make_purchase_bb()
        sku = link.split("=")[-1]
        if not is_in or "Sold Out" in description.split("\n"):
            in_stock = False
            self.printer.output(ctype, "OUT", "xxx", description, "", self.stream_mode, "BestBuy")
        else:
            in_stock = True
            print_desc = description[:20]
            if self.cards_to_find[ctype] is not None:
                if self.cards_to_find[ctype] and self.card_prices[ctype] > true_price:
                    self.printer.output(ctype, "IN", true_price,
                            print_desc, link, self.stream_mode, "BestBuy")
                    if self.settings.send_messages:
                        msg.send_message(self.number, "Card Found:  " + str(link))
                    if self.bb_info["bb_auto_buy"]:
                        buy = Purchase(self.driver, item, sku, "bestbuy", self.is_logged_in, self.logger, self.settings)
                        buy.make_purchase_bb()
            else:
                self.printer.output(ctype, "EXP", true_price,
                        print_desc, link, self.stream_mode, "BestBuy")

    async def loop_body(self, item):
        try:
            description = item.text
            link_item = item.find_element_by_class_name("sku-header")
            link = item.find_element_by_tag_name("a").get_attribute("href")

            parts = description.split("\n")
            cart_button = item.find_element_by_class_name("c-reviews-v4 ")
            nope = False

            if "Not yet reviewed" in cart_button.text:
                nope = True

            if len(parts) < 3 or "Sold Out" in parts[len(parts)-1] or nope:
                is_in = False
            else:
                is_in = True
            true_price = float(
                    re.sub(r'[^\d.]+', '', description.split('$')[1].strip()))

            #if self.debug:
            #    self.get_card(item, parts[0], "Test", true_price, is_in, link_item)

            for key in self.cards_to_find:
                if key in parts[0]:
                    self.card_count[key] += 1
                    self.total_prices[key] += 1
                    self.avg_prices[key] = self.total_prices[key] / self.card_count[key]
                    self.get_card(item, parts[0], key, true_price, is_in, link)
                    break

        except NoSuchElementException as e:
            if self.settings.save_logs:
                self.logger.log_info("Error in loop_body: {}".format(e))
            pass
        except  Exception as e:
            if self.settings.save_logs:
                self.logger.log_error("Error in loop_body: {}".format(e))
            pass
            
    async def validate_body(self, count, dt_string):
        try:
            if "" in self.driver.title:
                notice = self.driver.find_elements_by_class_name(
                    "item-info")
                total = self.driver.find_element_by_id("main-results")
                stock = total.find_elements_by_class_name("sku-item")
                self.item_count = len(stock)

                queue = []
                queue = asyncio.Queue()

                if not self.stream_mode:
                        if self.settings.show_progress_bar:
                            producers = [asyncio.create_task(self.loop_body(item)) for item in stock]
                        else:
                            producers = [asyncio.create_task(self.loop_body(item)) for item in stock]
                else:
                    if self.settings.show_price_line:
                        self.printer.print_refresh(count, dt_string, self.old_prices, self.avg_prices)
                    producers = [asyncio.create_task(self.loop_body(item)) for item in stock]

                await asyncio.gather(*producers)
                await queue.join()

                #with ThreadPoolExecutor(max_workers=len(stock)) as executor:
                #    if not self.stream_mode:
                #        if self.settings.show_progress_bar:
                #            {executor.submit(self.loop_body(item)): item for item in tqdm(stock)}
                #        else:
                #            {executor.submit(self.loop_body(item)): item for item in stock}
                #    else:
                #        self.printer.print_refresh(count, dt_string, self.old_prices, self.avg_prices)
                #        {executor.submit(self.loop_body(item)): item for item in stock}

                #sleep_interval = random.randrange(0, 1)
        except NoSuchElementException as e:
            if self.settings.save_logs:
                self.logger.log_info("Error in loop_body: {}".format(e))
            pass
        except  Exception as e:
            if self.settings.save_logs:
                self.logger.log_error("Error in loop_body: {}".format(e))
            pass

    def start(self):
        print("Started")
        count = 1
        try:
            self.check_country_page()
            self.close_deals_popup()
            self.close_feedback_popup()
            if self.login_at_start:
                self.login()
            while True:
                try:
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

                    #self.validate_body(count, dt_string)
                    asyncio.run(self.validate_body(count, dt_string))
                    page_num = 1
                    try:
                        self.driver.find_element_by_class_name("sku-list-page-next").click()
                        page_num += 1
                        #self.validate_body(count, dt_string)
                        asyncio.run(self.validate_body(count, dt_string))
                    except (TimeoutException, WebDriverException) as e:
                        self.driver.get(self.url)
                        pass
                    
                    count += 1
                    t1 = time.time()
                    diff = t1 - t0
                    self.total_time += diff
                    time_per_card = diff / self.item_count
                    if self.settings.show_refresh_time:
                        print("BestBuy Refresh Time: ", diff, " sec. Avg card check time: ", time_per_card)
                    #else:
                        #spinner.next()
                    if count % 3 == 0 and diff < 3:
                        break
                    # Prevent browser from slowing down by restarting it
                    if self.total_time >= 1200:
                        self.driver.close()
                        self.browser = Browser(self.settings)
                        self.driver = self.browser.driver
                        self.driver.get(self.url)
                        self.start()
                    else:
                        self.driver.refresh()
                except NoSuchElementException:
                    self.logger.log_error(
                        "Unable to find element. Refresh: " + str(count))
        except KeyboardInterrupt:
            self.driver.close()
            sys.exit()
