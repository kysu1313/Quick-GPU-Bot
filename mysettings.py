import json
from pathlib import Path
import os


class Settings:

    def __init__(
        self,
        use_firefox,
        custom_firefox_exe_path,
        use_chrome, 
        custom_chrome_exe_path,
        stream_mode, 
        instock_only_mode, 
        send_messages,
        show_progress_bar,
        show_refresh_time,
        purchase_multiple_items,
        load_images,
        headless_mode,
        save_logs,
        use_custom_urls,
        custom_urls,
        cards_to_find,
        card_prices,

        login_at_start,
        checkout_as_guest,

        bb_info,
        ne_info,
        az_info,
        shipping_info,
        payment_info,
        gmail_info
        ):

        # Settings
        self.use_firefox = self.str2bool(use_firefox)
        self.custom_firefox_exe_path = custom_firefox_exe_path
        self.use_chrome = self.str2bool(use_chrome)
        self.custom_chrome_exe_path = self.str2bool(custom_chrome_exe_path)
        self.stream_mode = self.str2bool(stream_mode)
        self.instock_only_mode = self.str2bool(instock_only_mode)
        self.send_messages = self.str2bool(send_messages)
        self.show_progress_bar = self.str2bool(show_progress_bar)
        self.show_refresh_time = self.str2bool(show_refresh_time)
        self.purchase_multiple_items = self.str2bool(purchase_multiple_items)
        self.load_images = self.str2bool(load_images)
        self.headless_mode = self.str2bool(headless_mode)
        self.save_logs = self.str2bool(save_logs)
        self.use_custom_urls = self.str2bool(use_custom_urls)
        self.custom_urls = custom_urls
        self.cards_to_find = cards_to_find
        self.card_prices = card_prices
        self.login_at_start = self.str2bool(login_at_start)
        self.checkout_as_guest = self.str2bool(checkout_as_guest)
        self.bb_info = bb_info
        self.ne_info = ne_info
        self.az_info = az_info
        self.shipping_info = shipping_info
        self.payment_info = payment_info
        self.gmail_info = gmail_info

        self.browser = self.getBrowser()
        self.clean_card_dict()

    def str2bool(self, st):
        return st == 'True'

    def clean_card_dict(self):
        for k in self.cards_to_find:
            v = self.cards_to_find[k]
            self.cards_to_find[k] = v == 'True' 

    def clean_info_dict(self):
        for k in self.bb_info:
            if "auto" in k:
                v = self.bb_info[k]
                self.bb_info[k] = v == 'True'
        for k in self.ne_info:
            if "auto" in k:
                v = self.ne_info[k]
                self.ne_info[k] = v == 'True'
        for k in self.az_info:
            if "auto" in k:
                v = self.az_info[k]
                self.az_info[k] = v == 'True'

    # Uses Firefox as default
    def getBrowser(self):
        if self.use_chrome == 'True':
            self.browser = 'chrome'
        else:
            self.browser = 'firefox'
        
    