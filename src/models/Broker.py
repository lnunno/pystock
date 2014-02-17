'''
Created on Feb 16, 2014

@author: lnunno
'''

from collections import defaultdict

class Broker(object):
    '''
    @var funds: Amount of cash available for buying stocks.
    @var holdings: A dictionary from stock to number of shares held. Defaults to 0 when no stocks are held.
    '''


    def __init__(self, initial_funds):
        '''
        Constructor
        '''
        self.funds = initial_funds
        self.holdings = defaultdict(int)
    
    def buy_stock(self, stock, num_shares, time):
        price = stock.get_price_at_time(time)
        print price 
    
    def sell_stock(self, stock, num_shares, time):
        price = stock.get_price_at_time(time)
