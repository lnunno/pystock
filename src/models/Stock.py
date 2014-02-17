'''
Created on Feb 16, 2014

@author: lnunno
'''

import ystockquote as ys

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
    
    def get_price_at_time(self, time):
        '''
        Get the closing price of the stock for the given day.
        '''
        p = ys.get_historical_prices(self.symbol, time, time)[time]
        return p[self.CLOSING_PRICE]
    
    def __hash__(self):
        return hash(self.symbol)
    
    def __eq__(self,other):
        return self.symbol == other.symbol
    
    def __ne__(self,other):
        return self.symbol != other.symbol    
