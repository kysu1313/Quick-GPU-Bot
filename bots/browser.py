from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

class Browser():
    def __init__(self, settings):
        # Custom settings
        self.load_images = settings.load_images
        self.headless_mode = settings.headless_mode
        self.save_logs = settings.save_logs
        self.use_custom_urls = settings.use_custom_urls
        self.custom_urls = settings.custom_urls
        self.settings = settings

        self.driver = self.get_driver()

    def str2bool(self, str):
        return str.lower() == 'true'

    def get_driver(self):
        if self.use_custom_urls:
            self.url = self.custom_urls
        if self.settings.browser == 'chrome':
            options = Options()
            options.binary_location(executable_path=self.settings.custom_chrome_exe_path)
            options.page_load_strategy = "eager"
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)
            if not self.load_images:
                prefs = {"profile.managed_default_content_settings.images": 2}
                options.add_experimental_option("prefs", prefs)
                options.add_argument("user-data-dir=.profile-bb")
            driver = webdriver.Chrome(options=options)
        else:
            fireFoxOptions = webdriver.FirefoxOptions()
            firefox_profile = webdriver.FirefoxProfile(self.settings.custom_firefox_exe_path)
            if self.headless_mode:
                fireFoxOptions.set_headless()
            elif not self.load_images:
                firefox_profile.set_preference('permissions.default.image', 2)
                firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
            driver = webdriver.Firefox(firefox_profile=firefox_profile, firefox_options=fireFoxOptions)
        return driver