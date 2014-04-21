'''
Created on Feb 16, 2014

@author: lnunno
'''

from datetime import datetime
from collections import OrderedDict
import matplotlib.pyplot as plt

class Stock(object):
    '''
    Model of a Stock.
    '''
    CLOSING_PRICE = 'Close'


    def __init__(self, symbol):
        '''
        Constructor
        '''
        self.symbol = symbol
    
    def get_price_at_date(self, date):
        '''
        Get the closing price of the stock for the given day.
        '''
        date_str = date.isoformat()
        p = ys.get_historical_prices(self.symbol, date_str, date_str)[date_str]
        return float(p[self.CLOSING_PRICE])
    
    def _sort_historical_prices(self,price_dict):
        date_ls = [self._iso_to_date(s) for s in price_dict.keys()]
        date_ls.sort()
        ord_dict = OrderedDict()
        for d in date_ls:
            ord_dict[d.isoformat()] = price_dict[d.isoformat()]
        return ord_dict
    
    def get_prices_for_date_range(self,start_date,end_date):
        price_dict = ys.get_historical_prices(self.symbol, start_date.isoformat(), end_date.isoformat())
        ord_price_dict = self._sort_historical_prices(price_dict)
        d = OrderedDict()
        for k,v in ord_price_dict.items():
            d[k] = v[self.CLOSING_PRICE]
        return d
    
    def _iso_to_date(self,s):
        return datetime.strptime(s,'%Y-%m-%d').date()
    
    def plot_price(self,start_date,end_date):
        price_dict = self.get_prices_for_date_range(start_date, end_date)
        date_ls = [(self._iso_to_date(x),price) for x,price in price_dict.items()]
        date_ls.sort()
        print date_ls
    
    def __str__(self):
        return '%s' % (self.symbol)
    
    def __hash__(self):
        return hash(self.symbol)
    
    def __eq__(self, other):
        return self.symbol == other.symbol
    
    def __ne__(self, other):
        return self.symbol != other.symbol