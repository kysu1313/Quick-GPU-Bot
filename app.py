from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import re
from colorama import Fore, Style, init
import os
from bots import NewEgg

NEWEGG_URL = "https://www.newegg.com/p/pl?d=rtx+3090&cm_sp=KeywordRelated-_-rtx%203080-_-rtx%203090-_-INFOCARD"


if __name__=="__main__":
    egg = NewEgg(NEWEGG_URL)

    try:
        egg.start()
    except KeyboardInterrupt:
        pass


