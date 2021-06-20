
from colorama import Fore, Style, init

class Printer():

    def __init__(self):
        self.old_prices = {}
        self.avg_prices = {}

    def output(self, ctype, success, price, details, link, stream_mode, platform):
        if success == "IN":
            self.pretty_print(Fore.GREEN, success, price, ctype, platform, details, link)
            # We found one in stock!
            #self.found_product(ctype, link)
        elif stream_mode:
            if success == "EXP":
                self.pretty_print(Fore.YELLOW, success, price, ctype, platform, details, link)
            elif success == "OUT":
                self.pretty_print(Fore.RED, success, price, ctype, platform, details, link)
            else:
                print("No data found")
        Style.RESET_ALL

    def print_message(self, color, message):
        print(color, message)

    def pretty_print(self, color, success, price, ctype, platform, detail, link):
        print(color + success, end=" ")
        if 'Ti' not in ctype:
            print(" | ${}  | {}    | {} | {} | {}".format(
                price, ctype, platform, detail.split("\n")[0], link))
        else:
            print(" | ${}  | {} | {} | {} | {}".format(
                price, ctype, platform, detail.split("\n")[0], link))

    def print_refresh(self, count, dt_string, avg_prices, old_prices):
        self.old_prices = old_prices
        self.avg_prices = avg_prices
        print('\n<=======================BestBuy Refresh #:{}, {}=======================>\n'.format(
                    count, dt_string), self.print_stats())

    def print_stats(self):
        print(Fore.YELLOW, "Average Prices:")
        for key in self.old_prices:
            if self.old_prices[key] > self.avg_prices[key]:
                print(Fore.GREEN, "{} ${:.2f}".format(key, self.avg_prices[key]), end=" ")
            else:
                print(Fore.YELLOW, "{} ${:.2f}".format(key, self.avg_prices[key]), end=" ")