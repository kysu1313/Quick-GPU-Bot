from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import re
from colorama import Fore, Style, init
import os
from bots import newegg, bestbuy, messenger
import logging
import threading

# "https://www.newegg.com/p/pl?N=100007709%20601357247%20601357248"
NEWEGG_URL = "https://www.newegg.com/p/pl?N=100007709%20601357247%20601357248"
BEST_BUY_URL = "https://www.bestbuy.com/site/computer-cards-components/video-graphics-cards/abcat0507002.c?id=abcat0507002&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203080%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203090"
threads = list()
THREAD_X = None
THREAD_Y = None

def newegg_run(one, number, mode):
    egg = newegg.NewEgg(NEWEGG_URL, number, mode)
    egg.start()

def bestbuy_run(one, number, mode):
    best = bestbuy.BestBuy(BEST_BUY_URL, number, mode)
    best.start()

def run_test(number, mode):
    # egg = newegg.NewEgg(NEWEGG_URL, number, mode)
    best = bestbuy.BestBuy(BEST_BUY_URL, bot, mode)
    # egg.start()
    best.start()

def run_all(one, number, mode):
    logging.info("Thread {}: starting".format("Newegg"))
    time.sleep(2)
    logging.info("Thread {}: starting".format("BestBuy"))
    THREAD_X = threading.Thread(target=newegg_run, args=(1,number, mode))
    threads.append(THREAD_X)
    THREAD_Y = threading.Thread(target=bestbuy_run, args=(1,number, mode))
    threads.append(THREAD_Y)
    THREAD_X.start()
    THREAD_Y.start()

if __name__=="__main__":
    # egg = newegg.NewEgg(NEWEGG_URL)
    # best = bestbuy.BestBuy(BEST_BUY_URL)
    number = "3362091264"
    try:
        # bot = messenger.Bot()
        bot = ""
        print("Mode 1: stream, Mode 2: only in stock")
        mode = input("Mode: ")
        print("\n<=============== INITIALIZING ===============>")
        # bot.login('13362091264')
        # run_test(number, mode)
        run_all(1, number, mode)
        # best.start()
        # egg.start()
    except KeyboardInterrupt:
        THREAD_X.terminate()
        THREAD_Y.terminate()
        pass


