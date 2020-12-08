from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import random
import re
from colorama import Fore, Style, init
import os
from selenium.common.exceptions import NoSuchElementException
import requests
import re
from bots.messenger import Bot
import logging as logger


class NewEgg():


    def __init__(self, url, bot):

        init(convert=True)
        self.url = url
        self.bot = bot
        # self.text, self.chat = bot.get_last_chat_id_and_text(bot.get_updates())
        


    # Pass xpath of popup close button
    def close_popup(self, driver, path):

        self.driver.find_element_by_xpath(path).click()


    def output(self, ctype, success, price, details, link):

        site = "Newegg"
        if success == "IN":
            print(Fore.GREEN + success, end =" ") 
            print(" STOCK!: ${}  | {} | {} | {}\n{}".format(price, ctype, site, details, link))
            self.bot.send_message(link)
            # try:
            #     bot.polling(none_stop=True)
            #     self.bot.send_message(self.text, self.chat)
            # except Exception as e:
            #     logger.error(e)
            #     time.sleep(15)
            
        elif success == "EXP":
            print(Fore.YELLOW + success, end =" ") 
            print(": ${}  | {} | {} | {}".format(price, ctype, site, details))
        elif success == "OUT":
            print(Fore.RED + success, end =" ") 
            print("OF STOCK: ${}  | {} | {} | {}".format(price, ctype, site, details))
        else:
            print("No data found")
        print(Style.RESET_ALL)


    def get_chunks(self, desc):

        chunks, chunk_size = len(desc), len(desc)//4
        pts = [desc[i:i+chunk_size] for i in range(0, chunks, chunk_size)]
        return pts[0]


    def get_card(self, item, description, ctype):

        try:
            sold_out = item.find_element_by_class_name("item-promo")
            sold_out = sold_out.text
        except NoSuchElementException:
            sold_out = "SOLD_OUT"
        display_desc = self.get_chunks(description.text)
        is_in_stock = True
        price = item.find_element_by_class_name("price-current")
        link = description.get_attribute("href")
        if "SOLD OUT" in sold_out or price.text == '':
            in_stock = False
            self.output(ctype, "OUT", "xxx", display_desc, link)
        else:
            in_stock = True
            print(price.text)
            true_price = float(re.sub(r'[^\d.]+', '', price.text.split('$')[1].strip()))
            if ctype == "3080" and true_price < 1100:
                self.output(ctype, "IN", true_price, display_desc, link)
            elif ctype == "3090" and true_price < 1900:
                self.output(ctype, "IN", true_price, display_desc, link)
            else:
                self.output(ctype, "EXP", true_price, display_desc, link)

    def select_dropdown(self, driver):
        drop = driver.find_elements_by_class_name("form-select")
        # print("len: ", len(drop), drop[1].text)
        drop[1].find_element(By.XPATH, "//*[@value='96']/option[text()='96']").click
        print(drop[1].find_element(By.XPATH, "//*[@value='96']/option[text()='96']"))
        # drop[1].find_element_by_text("96").click()

    def start(self):

        driver = webdriver.Firefox()
        driver.get(self.url)
        count = 1
        try:
            while True:
                t0 = time.time()
                print('\n=======================\Refresh #:{}\n======================='.format(count))
                # self.select_dropdown(driver)
                if ("3080" or "3090" in driver.title):
                    notice = driver.find_elements_by_class_name("item-info")
                    stock = driver.find_elements_by_class_name("item-container")
                    is80 = False
                    is90 = False
                    for item in stock:
                        description = item.find_element_by_class_name("item-title")
                        if "3080" in description.text:
                            self.get_card(item, description, "3080")
                        elif "3090" in description.text:
                            self.get_card(item, description, "3090")
                        time.sleep(random.uniform(0, 1))

                    sleep_interval = 5+random.randrange(0,1)
                    print()
                elif driver.find_element_by_class_name("popup-close") != None:
                    driver.find_element_by_class_name("popup-close").click()
                count += 1
                t1 = time.time()
                diff = t1 - t0
                print("diff: ", diff)
                if count % 3 == 0 and diff < 3:
                    break;
                driver.refresh()
        except KeyboardInterrupt:
            pass
