from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import re
from colorama import Fore, Style, init
import os
from bots import newegg, bestbuy, secret_messenger 
import logging
import threading

# "https://www.newegg.com/p/pl?N=100007709%20601357247%20601357248"
NEWEGG_URL = "https://www.newegg.com/p/pl?N=100007709%20601357247%20601357248"
BESTBUY_ALL_URL ="https://www.bestbuy.com/site/searchpage.jsp?st=rtx+3080&_dyncharset=UTF-8&_dynSessConf=&id=pcat17071&type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All+Categories&ks=960&keys=keys" 
#BEST_BUY_URL = "https://www.bestbuy.com/site/computer-cards-components/video-graphics-cards/abcat0507002.c?id=abcat0507002&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203080%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203090"
BESTBUY_3060_URL = "https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8&id=pcat17071&iht=y&keys=keys&ks=960&list=n&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203060%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203060%20Ti&sc=Global&st=rtx%20&type=page&usc=All%20Categories"
BESTBUY_3080_URL = "https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8&id=pcat17071&iht=y&keys=keys&ks=960&list=n&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203080&sc=Global&st=rtx%20&type=page&usc=All%20Categories"
BESTBUY_3090_URL = "https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8&id=pcat17071&iht=y&keys=keys&ks=960&list=n&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203090&sc=Global&st=rtx%20&type=page&usc=All%20Categories"

threads = list()
THREAD_X = None
THREAD_Y = None


def newegg_run(number, mode, login_mode, url):
    print("number: ", number)
    print("mode: ", mode)
    print("login_mode: ", login_mode)
    print("url: ", url)
    egg = newegg.NewEgg(number, mode, url)
    egg.start()


def bestbuy_run(number, mode, login_mode, url):
    best = bestbuy.BestBuy(number, mode, login_mode, url)
    best.start()


def run_test(number, mode, login_mode, url):

    print("number: ", number)
    print("mode: ", mode)
    print("login_mode: ", login_mode)
    print("url: ", url)
    print("Loading https://www.bestbuy.com.")
    egg = newegg.NewEgg(number, mode, NEWEGG_URL)
    print("Loading https://www.newegg.com.")
    best = bestbuy.BestBuy(bot, mode, login_mode, url)
    egg.start()
    best.start()


def signin_mode(input):
    if input == '1':
        return True
    else:
        return False


def parse_url(input):
    if input == '6':
        return BESTBUY_3060_URL
    elif input == '8':
        return BESTBUY_3080_URL
    elif input == '9':
        return BESTBUY_3090_URL
    else:
        return BESTBUY_ALL_URL


def run_all(number, mode, login_mode, url):
    logging.info("Thread {}: starting".format("Newegg"))
    time.sleep(2)
    logging.info("Thread {}: starting".format("BestBuy"))
    THREAD_X = threading.Thread(
        target=newegg_run, args=(number, mode, login_mode, url))
    threads.append(THREAD_X)
    THREAD_Y = threading.Thread(
        target=bestbuy_run, args=(number, mode, login_mode, url))
    threads.append(THREAD_Y)
    THREAD_X.start()
    THREAD_Y.start()


if __name__ == "__main__":
    # egg = newegg.NewEgg(NEWEGG_URL)
    # best = bestbuy.BestBuy(BEST_BUY_URL)
    number = "3362091264"
    try:
        # bot = messenger.Bot()
        bot = ""
        print("Mode 1: stream, Mode 2: only in stock")
        mode = input("Mode: ")

        print("\nEnter (1) to sign-in with a Google Account, or (2) if you want to sign-in with email and PW.")
        login_mode = input("Login (1/2): ")

        print("\nEnter (6) for 3060, Enter (8) for 3080, Enter (9) for 3090, Enter (A) for All")
        watchu_want = input("I want: ")

        print("\n<=============== INITIALIZING ===============>")
        # bot.login('13362091264')
        #run_test(number, mode, signin_mode(login_mode), parse_url(watchu_want))
        run_all(number, mode, signin_mode(login_mode), parse_url(watchu_want))
        # best.start()
        # egg.start()
    except KeyboardInterrupt:
        THREAD_X.terminate()
        THREAD_Y.terminate()
        pass
