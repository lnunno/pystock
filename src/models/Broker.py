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
    
    def buy_stock(self, stock, amt, time):
        price = stock.get_price_at_time(time)
        transaction_cost = price * amt
        if transaction_cost > self.funds:
            print 'Warning: tried to buy stock with inadequate funds! Transaction cancelled!'
            return
        self.holdings[stock] += amt
        self.funds -= transaction_cost
        
    def sell_stock(self, stock, amt, time):
        shares_held = self.holdings[stock]
        if shares_held < amt:
            print "Error: tried to sell more shares than were held! Had %d sold %d. Transaction cancelled!" % (shares_held,amt)
            return
        self.holdings[stock] -= amt
        price = stock.get_price_at_time(time)
        self.funds += price * amt