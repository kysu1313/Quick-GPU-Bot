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

NEWEGG_URL = "https://www.newegg.com/p/pl?N=100007709%20601357247%20601357248"
BEST_BUY_URL = "https://www.bestbuy.com/site/computer-cards-components/video-graphics-cards/abcat0507002.c?id=abcat0507002&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203080%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203090"
threads = list()

def newegg_run(one, bot):
    egg = newegg.NewEgg(NEWEGG_URL, bot)
    egg.start()

def bestbuy_run(one, bot):
    best = bestbuy.BestBuy(BEST_BUY_URL, bot)
    best.start()

def run_test(bot):
    # egg = newegg.NewEgg(NEWEGG_URL, bot)
    best = bestbuy.BestBuy(BEST_BUY_URL, bot)
    # egg.start()
    best.start()

def run_all(one, bot):
    logging.info("Thread {}: starting".format("Newegg"))
    time.sleep(2)
    logging.info("Thread {}: starting".format("BestBuy"))
    x = threading.Thread(target=newegg_run, args=(1,bot))
    threads.append(x)
    y = threading.Thread(target=bestbuy_run, args=(1,bot))
    threads.append(y)
    x.start()
    y.start()

if __name__=="__main__":
    # egg = newegg.NewEgg(NEWEGG_URL)
    # best = bestbuy.BestBuy(BEST_BUY_URL)

    try:
        bot = messenger.Bot()
        bot.login('13362091264')
        run_test(bot)
        # run_all(bot)
        # best.start()
        # egg.start()
    except KeyboardInterrupt:
        pass


