from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from concurrent.futures.thread import ThreadPoolExecutor
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from asciimatics.screen import ManagedScreen
from selenium.webdriver.common.by import By
from contextvars import ContextVar, Context
from requests.adapters import HTTPAdapter
from colorama import Fore, Style, init
from bots.textbox import TextEntry
from bots.purchase import Purchase 
from bots import messenger as msg
from bots.printer import Printer 
from bots.browser import Browser 
from bots.logger import Logger
from bots.fakeai import FakeAI
import scipy.interpolate as si
from selenium import webdriver
from dotenv import load_dotenv
from datetime import datetime
from time import sleep
from tqdm import tqdm
import numpy as np
import requests
import requests
import logging
import asyncio
import random
import time
import re
import os
import re
import sys

#NEWEGG_PDP_URL = "https://api.bestbuy.com/click/5592e2b895800000/{sku}/pdp"
#NEWEGG_CART_URL = "https://api.bestbuy.com/click/5592e2b895800000/{sku}/cart"
#NEWEGG_ADD_TO_CART = "https://secure.newegg.com/Shopping/AddToCart.aspx?Submit=ADD&ItemList={sku}"

#DEFAULT_HEADERS = {
#    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
#    "accept-encoding": "gzip, deflate, br",
#    "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
#    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
#    "origin": "https://www.newegg.com",
#}

MAX_TIMEOUT = 10

class NewEgg():

    def __init__(self, number, url, settings, debug):

        load_dotenv()
        init(convert=True)
        fhandler = logging.FileHandler(filename='.\\neweggLog.log', mode='a')
        self.logger = Logger(fhandler)
        #self.session = requests.Session()
        self.is_logged_in = False
        self.login_method_has_run = False
        self.DEBUG_MODE = settings.DEBUG_MODE
        self.debug = settings.debug
        self.printer = Printer()
        self.items_per_page = "&PageSize=90"
        self.settings = settings
        
        
        if settings is not None:
            self.MAX_TIMEOUT = self.settings.max_timeout
        else:
            self.MAX_TIMEOUT = MAX_TIMEOUT

        # General settings
        self.settings = settings
        self.url = url + self.items_per_page
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
            self.avg_prices[key] = \
            self.total_prices[key] = \
            self.card_count[key] = \
            self.old_prices[key] = 0.0
        self.viewed_cards = {}

        # NewEgg settings
        self.ne_info = settings.ne_info

        self.number = number
        self.sku_id = sku_id = None
        self.item_count = 0

        # Browser driver
        self.browser = Browser(settings)
        self.driver = self.browser.driver
        self.driver.get(url)

    def close_popup(self, path):
        """ Close popup window """
        self.driver.find_element_by_xpath(path).click()

    def get_timeout(self, timeout=MAX_TIMEOUT):
        return time.time() + timeout

    def login(self):
        timeout = self.get_timeout()
        if not self.login_method_has_run:
            self.login_method_has_run = True
            while True:
                try:
                    if self.DEBUG_MODE and not self.debug["login_enabled"]:
                        return
                    if self.driver.find_element_by_class_name('nav-complex-title').text == "Sign in / Register":
                        self.driver.find_element_by_xpath("//*[contains(text(), 'Sign in / Register')]").click()
                        WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "signin-title"))
                        )
                        self.driver.find_element_by_id("labeled-input-signEmail").send_keys(self.settings.ne_info['ne_email'])
                        self.driver.find_element_by_id("signInSubmit").click()

                        time.sleep(2)

                        if self.driver.find_element_by_class_name("signin-title").text == "Security Code":
                            self.enter_2fa()
                        

                        self.browser.driver_wait(By.ID, "labeled-input-password")
                        self.driver.find_element_by_id("labeled-input-password").send_keys(self.settings.ne_info['ne_password'])
                        self.driver.find_element_by_id("signInSubmit").click()
                
                except NoSuchElementException as e:
                    try:
                        if self.driver.find_element_by_xpath("""//*[contains(text(), 'Are you a human?')]"""):
                            self.captcha_try()
                    except NoSuchElementException:
                        pass
                    if self.settings.save_logs:
                        self.logger.log_info("Element not found in login(): {}".format(e))
                    pass
                except Exception as e:
                    if self.settings.save_logs:
                        self.logger.log_info("Error during login: {}".format(e))
                    pass
                self.is_logged_in = True
                if time.time() > timeout:
                    break

    def captcha_try(self):
        while True:
            try:

                if self.driver.find_element_by_xpath("""//*[contains(text(), 'Are you a human?')]"""):
                    element = self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/p[5]/a")
                    # //*[@id="playAudio"]
                    ai = FakeAI(self.driver)
                    ai.move_cursor(element)
            except NoSuchElementException:
                pass
            except Exception as e:
                if self.settings.save_logs:
                    self.logger.log_error("Error passing captcha: {}".format(e))
                break

    def enter_2fa(self, screen=None):
        self.printer.print_message(Fore.CYAN, "\n -------- PLEASE ENTER Newegg 2FA Code!!! -------- \n")
        while True:
            try:
                number = None

                # Show popup for 2FA code if running headless
                if self.settings.headless_mode or self.DEBUG_MODE:
                    popup = TextEntry()
                    popup.showField()
                    number = popup.getTextInput()

                val = ""

                if number != '' and number != None:
                    element = self.driver.find_element_by_xpath("""//*[@id="app"]/div/div[2]/div[2]/div/div/div[3]/form/div/div[3]/div/input[1]""").send_keys(number)

                try:
                    txt_area = self.driver.find_element_by_class_name("form-v-code")
                    val = txt_area.find_element_by_xpath("""//*[@id="app"]/div/div[2]/div[2]/div/div/div[3]/form/div/div[3]/div/input[6]""").get_attribute("value")
                except Exception as e:
                    if self.settings.save_logs:
                        self.logger.log_info("2FA text area not accessible, {}".format(e))
                    pass

                if val != None and val != "":
                    self.driver.find_element_by_id("signInSubmit").click()
                    break
                try:
                    self.driver.find_element_by_class_name("signin-title")
                except NoSuchElementException:
                    if self.driver.find_element_by_xpath("""//*[contains(text(), 'Are you a human?')]"""):
                        self.captcha_try()
                    break
            except NoSuchElementException:
                    if self.driver.find_element_by_xpath("""//*[contains(text(), 'Are you a human?')]"""):
                        self.captcha_try()
                    break
            except Exception as e:
                if self.settings.save_logs:
                    self.logger.log_info("Not on security code page anymore: {}".format(e))
                break

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
                sold_out = item.find_element_by_class_name("item-promo").text
            except NoSuchElementException:
                try:
                    sold_out = item.find_element_by_class_name("btn-mini").text
                except NoSuchElementException:
                    sold_out = "possibly"

            sku = link.split("=")[-1]
            
            self.card_count[ctype] += 1.0
            self.total_prices[ctype] += true_price
            self.avg_prices[ctype] = self.total_prices[ctype] / self.card_count[ctype]
            if sold_out == 'OUT OF STOCK' or sold_out == 'View Details ':
                in_stock = False
                self.printer.output(ctype, "OUT", "xxx", display_desc, "", self.stream_mode, "Newegg")
            else:
                in_stock = True
                print_desc = description.text[:20]
                if description.text in self.viewed_cards and self.viewed_cards[str(description.text)]+600 > time.time():
                    pass
                elif description.text in self.viewed_cards and self.viewed_cards[str(description.text)]+600 < time.time():
                    del self.viewed_cards[str(description.text)]
                elif self.cards_to_find[ctype] is not None:
                    if self.cards_to_find[ctype] and true_price < self.card_prices[ctype]:
                        self.viewed_cards[str(description.text)] = time.time()
                        self.printer.output(ctype, "IN", true_price,
                                print_desc, link, self.stream_mode, "NewEgg") 
                        if self.settings.send_messages:
                            msg.send_message(self.number, "Card Found:  " + str(link))
                        if self.DEBUG_MODE and self.debug["test_payment_no_purchase"]:
                            buy = Purchase(self.driver, item, sku, "newegg", self.is_logged_in, self.logger, self.settings)
                            buy.make_purchase_ne()
                        elif self.settings.ne_info["ne_auto_buy"]:
                            buy = Purchase(self.driver, item, sku, "newegg", self.is_logged_in, self.logger, self.settings)
                            buy.make_purchase_ne()
                else:
                    self.printer.output(ctype, "EXP", true_price,
                            print_desc, link, self.stream_mode, "NewEgg")
    
        except NoSuchElementException:
            try:
                if self.driver.find_element_by_xpath("""//*[contains(text(), 'Are you a human?')]"""):
                    self.captcha_try()
            except NoSuchElementException:
                pass
            pass
        except Exception as e:
            if self.settings.save_logs:
                self.logger.log_info("Error in get_card: {}".format(e))
            pass

    def select_dropdown(self):
        timeout = self.get_timeout()
        while True:
            try:
                drop = self.driver.find_elements_by_class_name("form-select")
                drop[1].find_element(
                    By.XPATH, "//*[@value='96']/option[text()='96']").click
                break
            except NoSuchElementException:
                pass
            except Exception as e:
                if self.settings.save_logs:
                    self.logger.log_info("Error in select_dropdown: {}".format(e))
                pass

            if time.time() > timeout:
                break

    async def loop_body(self, item):
        try:

            if item.text == '':
                return

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

            for key in self.cards_to_find:
                if key in description.text:
                    self.get_card(item, description, key, is_in, link, display_desc, true_price)
                    break
        except NoSuchElementException:
            try:
                if self.driver.find_element_by_xpath("""//*[contains(text(), 'Are you a human?')]"""):
                    self.captcha_try()
            except NoSuchElementException:
                pass
            pass
        except Exception as e:
            if self.settings.save_logs:
                self.logger.log_info("Error in loop_body: {}".format(e))
            pass


    async def validate_body(self, count, dt_string):
        try:
            if "" in self.driver.title:
                notice = self.driver.find_elements_by_class_name(
                    "item-info")
                stock = self.driver.find_elements_by_class_name(
                    "item-container")
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

            sleep_interval = random.randrange(0, 2)
            if self.driver.find_element_by_class_name("popup-close") != None:
                self.driver.find_element_by_class_name(
                    "popup-close").click()
        
        except NoSuchElementException:
            try:
                if self.driver.find_element_by_xpath("""//*[contains(text(), 'Are you a human?')]"""):
                    self.captcha_try()
            except NoSuchElementException:
                pass
            pass
        except Exception as e:
            if self.settings.save_logs:
                self.logger.log_info("Error in loop_body: {}".format(e))
            pass

    def start(self):

        self.driver.get(self.url + "&PageSize=96")

        
        #gm = Gmail(self.settings)

        self.login()
        self.select_dropdown()
        count = 1
        try:
            while True:
                t0 = time.time()
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

                delay = 3 # seconds
                try:
                    myElem = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'newegg-feedback')))
                    print("Page is ready")
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
                        msg = msg.join("{}: ${}, {}".format(key, str(self.avg_prices[key]), str(count)))
                    msg = msg.join('Iterations: {}'.format(str(count)))
                    self.logger.log_info(msg)

                asyncio.run(self.validate_body(count, dt_string))

                count += 1
                t1 = time.time()
                diff = t1 - t0
                time_per_card = diff / (self.item_count + 1)
                if self.settings.show_refresh_time:
                    print("Newegg Refresh Time: ", diff, " sec. Avg card check time: ", time_per_card)
                if count % 3 == 0 and diff < 3:
                    break
                self.driver.refresh()
        except NoSuchElementException:
            try:
                if self.driver.find_element_by_xpath("""//*[contains(text(), 'Are you a human?')]"""):
                    self.captcha_try()
            except NoSuchElementException:
                pass
            pass
        except Exception as e:
            if self.settings.save_logs:
                self.logger.log_info("Error in loop_body: {}".format(e))
            pass
        except KeyboardInterrupt:
            self.driver.close()
            sys.exit()
