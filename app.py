from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random



def close_popup(element):
    driver.find_element_by_id("popup-close").click()

# print(stock)
driver = webdriver.Firefox()
driver.get("https://www.newegg.com/p/pl?d=rtx+3080")
while True:
    
    time.sleep(0.03)
    assert "3080" in driver.title
    if ("3080" in driver.title):
        # elem = driver.find_element_by_name("q")
        notice = driver.find_elements_by_class_name("item-info")
        stock = driver.find_elements_by_class_name("item-container")

        for item in stock:
            description = item.find_element_by_class_name("item-title")
            if "3080" in description.text:
                is_in_stock = True
                in_stock = item.find_element_by_class_name("item-promo")
                # if ("OUT" in in_stock.text):
                #     is_in_stock = False
                # else:
                price = item.find_element_by_class_name("price-current")

                print(description.text)
                print(in_stock.text, ": ", price.text,"\n\n")
                # children = item.find_elements_by_tag_name("li")
        break;
            # print(children)
        assert "No results found." not in driver.page_source
        driver.close()
        time.sleep(1+random.randrange(0,1))
    elif driver.find_element_by_class_name("popup-close") != None:
        driver.find_element_by_class_name("popup-close").click()

    time.sleep(3) 
    driver.refresh()