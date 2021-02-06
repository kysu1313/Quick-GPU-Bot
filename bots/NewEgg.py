from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from colorama import Fore, Style, init
from selenium import webdriver
from datetime import datetime
import bots.messenger as msg
import logging as logger
from time import sleep
from tqdm import tqdm
import requests
import random
import time
import re
import os
import re


class NewEgg():

    def __init__(self, url, number, mode):

        init(convert=True)
        self.url = url
        self.number = number
        self.mode = mode

    # Pass xpath of popup close button

    def close_popup(self, driver, path):
        """ Close popup window """

        self.driver.find_element_by_xpath(path).click()

    # Formatting output.

    def output(self, ctype, success, price, details, link):
        """ Format output """

        site = "Newegg"
        if success == "IN":
            print(Fore.GREEN + success, end=" ")
            print(" STOCK! | ${}  | {} | {} | {}\n{}".format(
                price, ctype, site, details, link))
            print(details, "\n", link)
            if ctype == "3080":
                msg.send_message(self.number, link)
        elif self.mode is '1':
            if success == "EXP":
                print(Fore.YELLOW + success, end=" ")
                print(": ${}  | {} | {} | {}".format(
                    price, ctype, site, details))
            elif success == "OUT":
                print(Fore.RED + success, end=" ")
                print("OF STOCK: ${}  | {} | {} | {}".format(
                    price, ctype, site, details))
            else:
                print("No data found")

        Style.RESET_ALL

    # Split objects into chunks for parsing.

    def get_chunks(self, desc):
        """ Break down description to extract only the first part. """

        chunks, chunk_size = len(desc), len(desc)//4
        pts = [desc[i:i+chunk_size] for i in range(0, chunks, chunk_size)]
        return pts[0]

    # Gets card objects

    def get_card(self, item, description, ctype):
        """ Sift through a list item and extrace card data. """

        # Get sold out tag if it exists
        try:
            sold_out = item.find_element_by_class_name("item-promo")
            sold_out = sold_out.text

        except NoSuchElementException:
            sold_out = "possibly"

        display_desc = self.get_chunks(description.text)
        is_in_stock = True
        price = item.find_element_by_class_name("price-current")
        link = description.get_attribute("href")

        if "OUT" in sold_out or price.text == '':
            in_stock = False
            self.output(ctype, "OUT", "xxx", display_desc, link)
        else:
            in_stock = True
            true_price = float(
                re.sub(r'[^\d.]+', '', price.text.split('$')[1].strip()))
            if ctype == "3080" and true_price < 1100:
                self.output(ctype, "IN", true_price, display_desc, link)
            elif ctype == "3090" and true_price < 1900:
                self.output(ctype, "IN", true_price, display_desc, link)
            else:
                self.output(ctype, "EXP", true_price, display_desc, link)

    # Select dropdown to view all items on same page.
    # This does not work properly.

    def select_dropdown(self, driver):
        drop = driver.find_elements_by_class_name("form-select")
        drop[1].find_element(
            By.XPATH, "//*[@value='96']/option[text()='96']").click
        print(drop[1].find_element(
            By.XPATH, "//*[@value='96']/option[text()='96']"))

    # Checks for GPU name in title element.

    def loop_body(self, item):
        description = item.find_element_by_class_name("item-title")
        if "3080" in description.text:
            self.get_card(item, description, "3080")
        elif "3090" in description.text:
            pass
            # self.get_card(item, description, "3090")
        time.sleep(random.uniform(0, 1))

    # Opens the web browser and begins scanning.

    def start(self):

        driver = webdriver.Firefox()
        driver.get(self.url)
        count = 1
        try:
            while True:
                t0 = time.time()
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                print('\n<=======================Newegg Refresh #:{}, {}=======================>'.format(
                    count, dt_string))
                if ("3080" or "3090" in driver.title):
                    notice = driver.find_elements_by_class_name("item-info")
                    stock = driver.find_elements_by_class_name(
                        "item-container")
                    is80 = False
                    is90 = False
                    if self.mode == "2":
                        for item in tqdm(stock):
                            self.loop_body(item)
                    else:
                        for item in stock:
                            self.loop_body(item)

                    sleep_interval = 5+random.randrange(0, 1)
                    # print()
                elif driver.find_element_by_class_name("popup-close") != None:
                    driver.find_element_by_class_name("popup-close").click()
                count += 1
                t1 = time.time()
                diff = t1 - t0
                print("diff: ", diff)
                if count % 3 == 0 and diff < 3:
                    break
                driver.refresh()
        except KeyboardInterrupt:
            pass
