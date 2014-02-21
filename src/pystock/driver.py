'''
Created on Feb 16, 2014

@author: lnunno
'''
from models.Broker import Broker
from models.Stock import Stock, fortune_500_stocks
import random
from numpy.random import normal
from math import ceil
from datetime import date

def random_transaction(broker, date):
    flip = random.choice([True])
    base_amt = 10
    if flip:
        stock = random.choice(fortune_500_stocks)
        buy_amt = ceil(base_amt + base_amt * normal())
        broker.buy_stock(stock, buy_amt, date)
        return
    else:
        stock = random.choice(broker.holdings.keys())
        buy_amt = base_amt + base_amt * normal()
        broker.sell_stock(stock, buy_amt, date)
        return

if __name__ == '__main__':
    google = Stock('GOOG')
    ff = fortune_500_stocks
    broker = Broker(10000)
    a = google.get_prices_for_date_range(date(2014,2,1), date(2014,2,10))
    google.plot_price(date(2014,2,1), date(2014,2,10))
    
    
