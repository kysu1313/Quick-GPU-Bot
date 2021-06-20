from selenium.webdriver.common.keys import Keys
from bots import newegg, bestbuy, amazon, messenger
from colorama import Fore, Style, init
from jsoncomment import JsonComment
from mysettings import Settings
from selenium import webdriver
import multiprocessing
import threading
import logging
import random
import time
import json
import re

import os


NEWEGG_URL = "https://www.newegg.com/p/pl?d=rtx+30+series&PageSize=96"
NEWEGG_TEST = "https://www.newegg.com/p/pl?d=gpu&N=50001441"
NEWEGG_TEST_2 = "https://www.newegg.com/p/pl?d=gpu&N=100007709&isdeptsrh=1"

BESTBUY_ALL_URL = "https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8&id=pcat17071&iht=y&keys=keys&ks=960&list=n&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203060%20Ti%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203070%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203080%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203090&sc=Global&st=rtx%20&type=page&usc=All%20Categories"
BESTBUY_3060_URL = "https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8&id=pcat17071&iht=y&keys=keys&ks=960&list=n&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203060%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203060%20Ti&sc=Global&st=rtx%20&type=page&usc=All%20Categories"
BESTBUY_3080_URL = "https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8&id=pcat17071&iht=y&keys=keys&ks=960&list=n&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203080&sc=Global&st=rtx%20&type=page&usc=All%20Categories"
BESTBUY_3090_URL = "https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8&id=pcat17071&iht=y&keys=keys&ks=960&list=n&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203090&sc=Global&st=rtx%20&type=page&usc=All%20Categories"

AMAZON_ALL_URL = "https://www.amazon.com/s?k=rtx+30+series+graphics+card&rh=n%3A284822&ref=nb_sb_noss"

BB_IN_STOCK_TEST = """https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8&id=pcat17071&iht=y&keys=keys&ks=960&list=n&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20GT%201030%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20GT%20710%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20GTX%201060%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20GTX%201650%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203060%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203060%20Ti%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203070%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203070%20Ti%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203080%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203080%20Ti%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203090&sc=Global&st=gpu&type=page&usc=All%20Categories"""
BB_TEST = "https://www.bestbuy.com/site/searchpage.jsp?st=gpu&_dyncharset=UTF-8&_dynSessConf=&id=pcat17071&type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All+Categories&ks=960&keys=keys"
BB_AMD_TEST = "https://www.bestbuy.com/site/computer-cards-components/video-graphics-cards/abcat0507002.c?id=abcat0507002&qp=chipsetmanufacture_facet%3DChipset%20Manufacture~AMD"
BB_instock_test2 = "https://www.bestbuy.com/site/computer-cards-components/video-graphics-cards/abcat0507002.c?id=abcat0507002"

threads = list()
THREAD_X = None
THREAD_Y = None



def newegg_run(number, url, settings, debug=False):
    egg = newegg.NewEgg(number, url, settings, debug)
    egg.start()


def bestbuy_run(number, url, settings, debug=False):
    best = bestbuy.BestBuy(number, url, settings, debug)
    best.start()


def amazon_run(number, url, settings):
    azn = amazon.Amazon(number, url, settings)
    azn.start()

def newegg_process_test(number, url, settings, debug=False):
    PROCESS_X = multiprocessing.Process(
        target=newegg_run, args=(number, NEWEGG_URL, settings, debug))
    PROCESS_X.start()
    PROCESS_X.join()

def run_test(number, url, settings):

    if 'best' in url:
        print("Loading https://www.bestbuy.com.")
    elif 'new' in url:
        print("Loading https://www.newegg.com.")
    #egg = newegg.NewEgg(number, url, settings)
    azon = amazon.Amazon(number, url, settings)
    #print("Loading https://www.newegg.com.")
    #best = bestbuy.BestBuy(number, url, settings)
    #egg.start()
    #best.start()
    azon.start()

def run_all(one, number, settings, debug=False):
    logging.info("Thread {}: starting".format("Newegg"))
    time.sleep(2)
    logging.info("Thread {}: starting".format("BestBuy"))
    
    PROCESS_X = multiprocessing.Process(
        target=newegg_run, args=(number, NEWEGG_URL, settings, debug))
    PROCESS_Y = multiprocessing.Process(
        target=bestbuy_run, args=(number, BESTBUY_ALL_URL, settings, debug))

    PROCESS_X.start()
    PROCESS_Y.start()
    PROCESS_X.join()
    PROCESS_Y.join()

def parse_settings():
    dir = os.getcwd() + '\\settings.json'
    f = open(dir, "r")
    json = JsonComment()
    data = json.loads(f.read())
    sett = Settings(**data.get('settings'))
    return sett

if __name__ == "__main__":
    # Your number here
    number = "1234567"
    try:

        print("\n<=============== INITIALIZING ===============>")

        settings = parse_settings()

        #bestbuy_run(number, BB_instock_test2, settings)
        #newegg_run(number, NEWEGG_URL, settings, True)
        #newegg_process_test(number, NEWEGG_URL, settings, True)
        #amazon_run(number, AMAZON_ALL_URL, settings, True)
        run_all(1, number, settings, True)

    except KeyboardInterrupt:
        print("Terminating ...")
        THREAD_X.terminate()
        THREAD_Y.terminate()
        pass
