'''
Created on Feb 16, 2014

@author: lnunno
'''
from models.Broker import Broker
from models.Stock import Stock
from models.Stock import fortune_500_stocks

if __name__ == '__main__':
    google = Stock('GOOG')
    broker = Broker(10000)
    broker.buy_stock(google, 1, '2014-02-14')
    print broker.funds
    ss = fortune_500_stocks
    for s in ss:
        print s
    