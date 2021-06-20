
from bots import messenger as msg
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import time
from datetime import date
from bots import messenger as msg
import sys
import imaplib
import imapclient
import email
from email.header import decode_header
import webbrowser
import os

NEWEGG_PDP_URL = "https://api.bestbuy.com/click/5592e2b895800000/{}/pdp"
NEWEGG_CART_URL = "https://api.bestbuy.com/click/5592e2b895800000/{}/cart"
NEWEGG_ADD_TO_CART = "https://secure.newegg.com/Shopping/AddToCart.aspx?Submit=ADD&ItemList={}"

BEST_BUY_PDP_URL = "https://api.bestbuy.com/click/5592e2b895800000/{}/pdp"
BEST_BUY_CART_URL = "https://api.bestbuy.com/click/5592e2b895800000/{}/cart"
BEST_BUY_ADD_TO_CART_API_URL = "https://www.bestbuy.com/cart/api/v1/addToCart"
BEST_BUY_CHECKOUT_URL = "https://www.bestbuy.com/checkout/c/orders/{}/"

DEFAULT_MAX_TIMEOUT = 10

BB_XPATH = {

    # Login Information
    "email_field": """//*[@id="fld-e"]""",
    "password_field": """//*[@id="fld-p1"]""",
    "guest_email_field": """//*[@id="user.emailAddress"]""",
    "guest_phone_field": """//*[@id="user.phone"]""",
    "checkout_login_btn": """/html/body/div[1]/div/section/main/div[2]/div[1]/div/div/div/div/form/div[3]/button""",

    # Shipping Information
    "shipping_v5": "//*[contains(@id, 'ui_address_5')]",
    "shipping_v2": "//*[contains(@id, 'ui_address_2')]",
    "firstname_field": """//*[@id="consolidatedAddresses.ui_address_{}.firstName"]""",
    "lastname_field": """//*[@id="consolidatedAddresses.ui_address_{}.lastName"]""",
    "street_address": """//*[@id="consolidatedAddresses.ui_address_{}.street"]""",
    "apartment": """//*[@id="consolidatedAddresses.ui_address_{}.street2"]""",
    "city": """//*[@id="consolidatedAddresses.ui_address_{}.city"]""",
    "state": "//select[@id='consolidatedAddresses.ui_address_{}.state']/option[text()='NC']",
    "zip": """//*[@id="consolidatedAddresses.ui_address_{}.zipcode"]""",
    "continue_to_billing": "//*[contains(text(), 'Continue to Payment Information')]",
    "switch_to_shipping": "//*[contains(text(), 'Switch to Shipping')]",

    # Payment Information
    "card_field": "//*[contains(@id, 'optimized-cc-card-number')]",
    "card_expiration_month": "expiration-month",
    "card_expiration_year": "expiration-year",
    "security_code": "credit-card-cvv",
    "place_order_btn": "//*[contains(text(), 'Place Your Order')]"
}

NE_XPATH = {

    # Add To Cart Btn   
    "cart_btn": "//*[contains(text(), 'Add to cart')]",
    "view_cart_and_checkout": "//*[contains(text(), 'View Cart & Checkout')]",
    "secure_checkout": "//*[contains(text(), 'Secure Checkout')]",
    "cart": "//*[contains(text(), 'Shopping Cart')]",
    "guest_checkout_btn": "//*[contains(text(), 'Continue With Guest Checkout')]",


    # Sign-in 
    "signin_label": "/html/body/div[5]/div/div[2]/div[2]/div/div/div[1]/div",
    "signin_email_field": """//*[@id="labeled-input-signEmail"]""",
    "password_field": """//*[contains(text(), 'Password')]""",
    "email_input": "/html/body/div[5]/div/div[2]/div[2]/div/div/div[1]/form[1]/div/div[1]/div/input",
    "signin_page_signin_btn": """//*[@id="signInSubmit"]""",

    # Shipping & Payment 
    "continue_to_delivery": """//*[contains(text(), 'Continue to delivery')]""",
    "delivery_speed": """//*[@id="DhlSmartMail3To7Days"]""",
    "continue_to_payment": """//*[contains(text(), 'Continue to payment')]""",
    "cvv_field": "mask-cvv-4",
    "review_order_btn": """//*[contains(text(), 'Review your order')]""",
    "card_number_review_label": """//*[contains(text(), 'Card Number')]""",
    "card_number_review_input": "/html/body/div[6]/div/div[2]/div[2]/div[2]/input"

}

class Purchase():
    def __init__(self, driver, item, sku, site, is_logged_in, logger, settings):
        self.driver = driver
        self.item = item
        self.sku = sku
        self.site = site
        self.is_logged_in = is_logged_in
        self.logger = logger
        self.settings = settings
        self.gmail_port = 993
        self.DEBUG_MODE = settings.DEBUG_MODE
        self.debug = settings.debug

    def make_purchase_bb(self):
        try:
            if self.sku is not None:
                self.driver.get(BEST_BUY_CART_URL.format(self.sku))
            else:
                self.item.find_element_by_class_name("add-to-cart-button").click()
                try:
                    self.driver_wait(By.CLASS_NAME, "c-modal-grid", max_wait=5)
                    webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
                except Exception:
                    pass

                self.driver_wait(By.CLASS_NAME, "cart-link")
                time.sleep(1)
                self.driver.find_element_by_class_name("cart-link").click()

            self.driver_wait(By.ID, "cartApp", max_wait=5)
            time.sleep(1)
            #self.driver.find_element_by_xpath("""//*[@id="cartApp"]/div[2]/div[1]/div/div[2]/div[1]/section[2]/div/div/div[3]/div/div[1]/button""").click()
            self.driver.find_element_by_class_name("checkout-buttons__checkout").find_element_by_class_name("btn").click()
            
            #self.driver_wait(By.CLASS_NAME, "cia-signin")

            try:
                self.driver_wait(By.CLASS_NAME, "checkout-header__title", max_wait=4)
                self.driver.find_element_by_class_name("checkout-header__title")
                self.fill_shipping_info_bb()
            except Exception as e:
                pass
            try:
                self.driver_wait(By.CLASS_NAME, "cia-actual-full-page-wrapper", max_wait=5)
                if self.settings.checkout_as_guest:
                    self.driver.find_element_by_class_name("guest").click()
                else:
                    try:
                        self.driver.find_element_by_xpath(BB_XPATH["email_field"]).send_keys(self.settings.bb_info["bb_email"])
                    except Exception:
                        pass
                    try:
                        self.driver_wait(By.CLASS_NAME, "tb-input", max_wait=5)
                        pw_field = self.driver.find_element_by_class_name("tb-input")
                        if pw_field.get_attribute('value') == None or pw_field.get_attribute('value') == "":
                            self.driver.find_element_by_class_name("tb-input").send_keys(self.settings.bb_info["bb_password"])
                    except Exception:
                        pass
                    self.driver.find_element_by_xpath(BB_XPATH["checkout_login_btn"]).click()
                self.select_shipping_bb()
                self.fill_shipping_info_bb()
            except Exception as e:
                pass

            self.fill_payment_info_bb()
            self.driver.find_element_by_xpath("/html/body/div[1]/main/div/div[2]/div[1]/div/div[1]/div[1]/section[2]/div/div/div[3]/div/div[1]/button").click()
            print("Item added to cart")
        except Exception as e:
            if self.settings.save_logs:
                self.logger.log_error("Exception Raised: {}".format(e))
            pass

    def make_purchase_ne(self):
        try:
            self.driver.find_element_by_xpath(NE_XPATH["cart_btn"]).click()
            self.driver_wait(By.CLASS_NAME, "message-title", max_wait=4)

            # TODO: Remove / Fix driver wait
            time.sleep(1)
            self.driver.find_element_by_xpath(NE_XPATH["view_cart_and_checkout"]).click()

            self.driver_wait(By.XPATH, NE_XPATH["cart"], max_wait=4)
            self.driver.find_element_by_xpath(NE_XPATH["secure_checkout"]).click()
            #if not self.is_logged_in:
            if self.settings.checkout_as_guest:
                self.driver_wait(By.CLASS_NAME, "signin-title", max_wait=4)
                self.driver.find_element_by_xpath(NE_XPATH["guest_checkout_btn"]).click()
            else:
                self.signin_ne()
            self.enter_delivery_info_ne()
            self.enter_payment_info_ne()
        except Exception as e:
            if self.settings.save_logs:
                self.logger.log_error("Exception Raised: {}".format(e))
            pass

    def signin_ne(self):
        try:
            self.driver_wait(By.CLASS_NAME, "signin-title", max_wait=4)
            if self.driver.find_element_by_id("labeled-input-signEmail").get_attribute("value") != self.settings.ne_info["ne_email"]:
                self.driver.find_element_by_id("labeled-input-signEmail").send_keys(self.settings.ne_info['ne_email'])
            # TODO: Remove / Replace with WebDriverWait
            time.sleep(1)
            self.driver.find_element_by_id("signInSubmit").click()
            

            try:
                self.driver_wait(By.XPATH, NE_XPATH["password_field"], max_wait=4)
                self.driver.find_element_by_id("labeled-input-password").send_keys(self.settings.ne_info['ne_password'])
            except Exception:
                pass

            self.driver.find_element_by_id("signInSubmit").click()
            #signin = self.driver.find_element_by_id("labeled-input-password").send_keys(self.settings.ne_info['ne_password'])

            self.driver.find_element_by_xpath(NE_XPATH["signin_page_signin_btn"]).click()
        except Exception:
            if self.settings.save_logs:
                self.logger.log_info("Failed during login")
            pass


    def enter_delivery_info_ne(self):
        # Continue to delivery
        try:
            self.driver_wait(By.CLASS_NAME, "checkout-step-action", max_wait=4)
            self.driver.find_element_by_xpath(NE_XPATH["continue_to_delivery"]).click()

            self.driver_wait(By.XPATH, NE_XPATH["continue_to_payment"], max_wait=4)
            self.driver.find_element_by_xpath(NE_XPATH["continue_to_payment"]).click()
        except Exception:
            if self.settings.save_logs:
                self.logger.log_info("Failed during delivery info entry")
            pass
    
    def driver_wait(self, id_type, text, max_wait=3):
        WebDriverWait(self.driver, max_wait).until(
            EC.presence_of_element_located((id_type, text))
        )
    
    def fill_shipping_info_bb(self):
        try:
            if self.settings.save_logs:
                msg = "Filling Shipping info, sku: {}".format(self.sku)
                self.logger.log_info(msg)

            self.driver_wait(By.CLASS_NAME, "streamlined__shipping", max_wait=4)
            #element = WebDriverWait(self.driver, 3).until(
            #            EC.presence_of_element_located((By.CLASS_NAME, "streamlined__shipping"))
            #)
            pd_id = 2
            try:
                # BestBuy has multiple shipping forms??
                ele = self.driver.find_element_by_xpath(BB_XPATH["shipping_v5"])
                if ele is not None:
                    pd_id = 5
            except NoSuchElementException as e:
                    print("Already on shipping info page.")

            if self.driver.find_element_by_xpath(BB_XPATH["firstname_field"].format(pd_id)).get_attribute('value') == "":
                self.text_entry(self.driver.find_element_by_xpath(BB_XPATH["firstname_field"].format(pd_id)), self.settings.shipping_info["first_name"])
            if self.driver.find_element_by_xpath(BB_XPATH["lastname_field"].format(pd_id)).get_attribute('value') == "":
                self.text_entry(self.driver.find_element_by_xpath(BB_XPATH["lastname_field"].format(pd_id)), self.settings.shipping_info["last_name"])
            if self.driver.find_element_by_xpath(BB_XPATH["street_address"].format(pd_id)).get_attribute('value') == "":
                self.text_entry(self.driver.find_element_by_xpath(BB_XPATH["street_address"].format(pd_id)), self.settings.shipping_info["address"])
            
            if self.settings.shipping_info["apartment"] == 'True':
                self.find_element_by_class_name("address-form__showAddress2Link").click()
                if self.driver.find_element_by_xpath(BB_XPATH["apartment"].format(pd_id)).get_attribute('value') == "":
                    self.text_entry(self.driver.find_element_by_xpath(BB_XPATH["apartment"].format(pd_id)), self.settings.shipping_info["apartment"])
            
            webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
            
            if self.driver.find_element_by_xpath(BB_XPATH["city"].format(pd_id)).get_attribute('value') == "":
                self.text_entry(self.driver.find_element_by_xpath(BB_XPATH["city"].format(pd_id)), self.settings.shipping_info["city"])
            self.driver.find_element_by_xpath(BB_XPATH["state"].format(pd_id)).click()
            if self.driver.find_element_by_xpath(BB_XPATH["zip"].format(pd_id)).get_attribute('value') == "":
                self.text_entry(self.driver.find_element_by_xpath(BB_XPATH["zip"].format(pd_id)), self.settings.shipping_info["zip_code"])
            
            if self.settings.checkout_as_guest:
                if self.driver.find_element_by_xpath(BB_XPATH["guest_email_field"]).get_attribute('value') is None or "":
                    self.driver.find_element_by_xpath(BB_XPATH["guest_email_field"]).send_keys(self.settings.bb_info["bb_email"])
                if self.driver.find_element_by_xpath(BB_XPATH["guest_phone_field"]).get_attribute('value') is None or "":
                    self.driver.find_element_by_xpath(BB_XPATH["guest_phone_field"]).send_keys(self.settings.shipping_info["phone_number"])
        except Exception as e:
            if self.settings.save_logs:
                self.logger.log_error("Exception Raised: {}".format(e))
            pass


    def enter_payment_info_ne(self):
        try:
            self.driver_wait(By.CLASS_NAME, "mask-cvv-4", max_wait=4)
            self.text_entry(self.driver.find_element_by_class_name(NE_XPATH["cvv_field"]), self.settings.payment_info["security_code"])
            self.driver.find_element_by_xpath(NE_XPATH["review_order_btn"]).click()

            try:
                self.driver_wait(By.XPATH, NE_XPATH["card_number_review_label"], max_wait=4)
                self.text_entry(self.driver.find_element_by_xpath(NE_XPATH["card_number_review_input"]), self.settings.payment_info["security_code"])
                self.driver.find_element_by_xpath(NE_XPATH["review_order_save"])
            except Exception as e:
                if self.settings.save_logs:
                    self.logger.log_info("Failed to find review order button{}".format(e))
                pass

            # If just testing, don't purchase anything
            if self.DEBUG_MODE and not self.debug["purchase_enabled"]:
                if self.settings.save_log:
                    self.logger.log_success("Demo Purchase Made")
                return

            try:
                self.driver_wait(By.ID, "btnCreditCard", max_wait=4)
                self.driver.find_element_by_id("btnCreditCard").click()
                self.logger.log_success("PURCHASE SUCCESSFUL")
                msg.send_message("GPU Order Placed, {}".format(self.driver.url))
            except Exception as e:
                if self.settings.save_logs:
                    self.logger.log_info("Failed to place order, {}".format(e))

        except Exception:
            if self.settings.save_logs:
                self.logger.log_info("Failed to enter payment info")
            pass


    def fill_payment_info_bb(self):
        timeout = self.get_timeout()
        log_msg = ""
        while True:
            try:
                if self.settings.save_logs:
                    msg = "Filling Payment info, sku: {}".format(self.sku)
                    self.logger.log_info(msg)

                self.driver.find_element_by_xpath(BB_XPATH["continue_to_billing"]).click()
                self.driver_wait(By.CLASS_NAME, "payment__cc-label", max_wait=4)
                #WebDriverWait(self.driver, 10).until(
                #        EC.presence_of_element_located((By.CLASS_NAME, "checkout__col"))
                #    )

                self.text_entry(self.driver.find_element_by_xpath(BB_XPATH["card_field"]), self.settings.payment_info["card_number"])
                select = Select(self.driver.find_element_by_name(BB_XPATH["card_expiration_month"]))
                select.select_by_value(self.settings.payment_info["expiration_month"])
                select = Select(self.driver.find_element_by_name(BB_XPATH["card_expiration_year"]))
                select.select_by_value(self.settings.payment_info["expiration_year"])
                self.text_entry(self.driver.find_element_by_id(BB_XPATH["security_code"]), self.settings.payment_info["security_code"])

                # If just testing, don't purchase anything
                if self.DEBUG_MODE and not self.debug["purchase_enabled"]:
                    return

                self.driver.find_element_by_xpath(BB_XPATH["place_order_btn"]).click()
                print("Order Placed")
                self.logger.log_success("PURCHASE SUCCESSFUL")
                msg.send_message("GPU Order Placed, {}".format(self.driver.url))

                if self.settings.save_logs:
                    msg = "Purchase Made, sku: {}, {}".format(self.sku, str(date.today()))
                    self.logger.log_info(msg)

                if not self.settings.purchase_multiple_items:
                    sys.exit()
            except Exception as e:
                if self.settings.save_logs and log_msg != e:
                    self.logger.log_error("Exception Raised during fill_payment_info_bb(): {}".format(e))
                log_msg = e
                pass
            if time.time() > timeout:
                break

    def text_entry(self, element, text):
        #action.MoveByOffset(x+10, y+10).Perform();  #moves cursor to point (5,5)
        #action.MoveByOffset(10, 15).Perform();  #moves cursor to point (10,15)
        try:
            x = element.rect["x"]
            y = element.rect["y"]
            action = ActionChains(self.driver);
            action.move_to_element(element)
            action.click(element)
            action.send_keys(text)
            #for ch in text:
            #    action.send_keys(element, ch)
            #    time.sleep(0.001)
            action.perform()
        except Exception as e:
            if self.settings.save_logs:
                self.logger.log_info("Key entry failed: {}".format(e))
            pass

    def get_timeout(self, timeout=DEFAULT_MAX_TIMEOUT):
        return time.time() + timeout

    def select_shipping_bb(self):
        try:
            self.driver.find_element_by_xpath(BB_XPATH["switch_to_shipping"]).click()

        except NoSuchElementException as e:
            if self.settings.save_logs:
                self.logger.log_error("Exception Raised: {}".format(e))

