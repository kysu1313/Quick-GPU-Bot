from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import re
from colorama import Fore, Style, init
import os


class BestBuy():


    def __init__(self, url):

        init(convert=True)
        self.url = url


    # Pass xpath of popup close button
    def close_popup(self, driver, path):

        self.driver.find_element_by_xpath(path).click()


    def output(self, ctype, success, price, details, link):

        platform = "BestBuy"
        if success == "IN":
            print(Fore.GREEN + success, end =" ") 
            print(" STOCK! | ${}  | {} | {} | {}".format(price, ctype, platform, details[0], link))
        elif success == "EXP":
            print(Fore.YELLOW + success, end =" ") 
            print(" | ${}  | {} | {} | {}".format(price, ctype, platform, details[0]))
        elif success == "OUT":
            print(Fore.RED + success, end =" ") 
            print("OF STOCK | ${}  | {} | {} | {}".format(price, ctype, platform, details[0]))
        else:
            print("No data found")
        print(Style.RESET_ALL)


    def get_chunks(self, desc):
        new_desc = desc.split("\n")[0]
        return new_desc


    def get_card(self, item, description, ctype, is_in):

        if not is_in or "Sold Out" in description.split("\n"):
            in_stock = False
            self.output(ctype, "OUT", "xxx", description.split("\n"), "link")
        else:
            in_stock = True
            true_price = float(re.sub(r'[^\d.]+', '', description.split('$')[1].strip()))
            if ctype == "3080" and true_price < 1100:
                self.output(ctype, "IN", true_price, description.split("\n"), "link")
            elif ctype == "3090" and true_price < 1900:
                self.output(ctype, "IN", true_price, description.split("\n"), "link")
            else:
                self.output(ctype, "EXP", true_price, description.split("\n"), "link")


    def start(self):

        driver = webdriver.Firefox()
        driver.get(self.url)
        count = 1
        try:
            while True:
                t0 = time.time()
                print('\n=======================\Refresh #:{}\n======================='.format(count))
                print(driver.title)
                # assert "3080" or "3090" in driver.title
                if ("3080" or "3090" in driver.title):
                    notice = driver.find_elements_by_class_name("item-info")
                    total = driver.find_element_by_id("main-results")
                    stock = total.find_elements_by_class_name("sku-item")
                    is80 = False
                    is90 = False
                    for item in stock:
                        description = item.text

                        # print(description.split("\n")[0]) # Description
                        # print(description.split("\n")[2]) # rating
                        # print(description.split("\n")[4]) # Sold Out
                        # print(description.split("\n")[8]) # price
                        # print(description.split("\n")[9])
                        # print(description.split("\n")[10])
                        # print(description.split("\n")[11])
                        # print(description.split("\n")[12])

                        parts = description.split("\n")
                        cart_button = item.find_element_by_class_name("c-reviews-v4 ")
                        nope = False
                        if "Not yet reviewed" in cart_button.text:
                            nope = True

                        if "Sold Out" in parts[4] or nope:
                            is_in = False
                        else:
                            is_in = True

                        if "3080" in parts[0]:
                            self.get_card(item, description, "3080", is_in)
                        elif "3090" in parts[0]:
                            self.get_card(item, description, "3090", is_in)
                        time.sleep(random.uniform(0, 1))

                    sleep_interval = 5+random.randrange(0,1)
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
