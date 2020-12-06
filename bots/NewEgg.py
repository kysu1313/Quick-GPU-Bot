from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import re
from colorama import Fore, Style, init
import os


class NewEgg():

    def __init__(self, url):
        init(convert=True)
        self.url = url
        self.driver = webdriver.Firefox()
        self.get_window()

    def get_window(self):
        self.driver.get(self.url)

    # Pass xpath of popup close button
    def close_popup(self, driver, path):
        self.driver.find_element_by_xpath(path).click()

    def output(self, type, success, price, details):
        if success == "IN":
            print(Fore.GREEN + success, end =" ") 
            print(":\t ${}  | {}".format(price, details))
        elif success == "EXP":
            print(Fore.YELLOW + success, end =" ") 
            print(":\t ${}  | {}".format(price, details))
        elif success == "OUT":
            print(Fore.RED + success, end =" ") 
            print(":\t ${}  | {}".format(price, details))
        else:
            print("No data found")
        print(Style.RESET_ALL)

    def start(self, good):
        count = 1
        try:
            while good:
                print('\n\=======================\\nLoop #:{}\n\=======================\\'.format(count))
                assert "3080" in driver.title
                if ("3080" in driver.title):
                    notice = driver.find_elements_by_class_name("item-info")
                    stock = driver.find_elements_by_class_name("item-container")
                    is80 = False
                    is90 = False
                    for item in stock:
                        description = item.find_element_by_class_name("item-title".format(count))
                        if "3080" in description.text:
                            is80 = True
                            is_in_stock = True
                            price = item.find_element_by_class_name("price-current")
                            if price.text == "":
                                in_stock = False
                                self.output(is80, "OUT", "xxx", description.text)
                            else:
                                in_stock = True;
                                true_price = float(re.sub(r'[^\d.]+', '', price.text.split('$')[1].strip()))
                                if true_price < 1100:
                                    self.output(is80, "IN", true_price, description.text)
                                else:
                                    self.output(is80, "EXP", true_price, description.text)
                        elif "3090" in description.text:
                            is90 = True
                            time.sleep(1)

                    
                        # print(children)
                    assert "No results found." not in driver.page_source
                    # driver.close()
                    sleep_interval = 5+random.randrange(0,1)
                    print("\n\n\n{}\n\n\n".format(sleep_interval))
                    time.sleep(sleep_interval)
                    print()
                elif driver.find_element_by_class_name("popup-close") != None:
                    driver.find_element_by_class_name("popup-close").click()
                sleep_interval = 1+random.randrange(0,1)
                print("\n\n\n{}\n\n\n".format(sleep_interval))
                time.sleep(sleep_interval)
                print()

                time.sleep(3) 
                count += 1
                driver.refresh()
        except KeyboardInterrupt:
            pass