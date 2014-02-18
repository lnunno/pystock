'''
Created on Feb 16, 2014

@author: lnunno
'''

from collections import defaultdict
from Transaction import Transaction

class Broker(object):
    '''
    @var funds: Amount of cash available for buying stocks.
    @var holdings: A dictionary from stock to number of shares held. Defaults to 0 when no stocks are held.
    '''


    def __init__(self, initial_funds):
        '''
        Constructor
        '''
        self.initial_funds = initial_funds
        self.funds = initial_funds
        self.holdings = defaultdict(int)
        
    def execute_transaction(self, transaction):
        if transaction.transaction_type == Transaction.buy:
            self.buy_stock(transaction.stock, transaction.amount, transaction.date) 
        elif transaction.transaction_type == Transaction.sell:
            self.sell_stock(transaction.stock, transaction.amount, transaction.date)
    
    def buy_stock(self, stock, amt, date):
        price = stock.get_price_at_date(date)
        transaction_cost = price * amt
        if transaction_cost > self.funds:
            print 'Warning: tried to buy stock with inadequate funds! Transaction cancelled!'
            return
        self.holdings[stock] += amt
        self.funds -= transaction_cost
        
    def sell_stock(self, stock, amt, date):
        shares_held = self.holdings[stock]
        if shares_held < amt:
            print "Error: tried to sell more shares than were held! Had %d sold %d. Transaction cancelled!" % (shares_held, amt)
            return
        self.holdings[stock] -= amt
        price = stock.get_price_at_date(date)
        self.funds += price * amt
        
    def profit(self):
        return self.funds - self.initial_funds
