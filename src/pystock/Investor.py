'''
Created on Feb 16, 2014

@author: lnunno
'''

from collections import defaultdict

class Investor(object):
    '''
    @var funds: Amount of cash available for buying stocks.
    @var holdings: A dictionary from stock to number of shares held. Defaults to 0 when no stocks are held.
    '''

    def __init__(self, initial_funds, start_date):
        '''
        @param initial_funds: The amount of cash that the Investor has available to invest initially.
        @param start_date: The point in time that an Investor begins investing. 
        '''
        self.initial_funds = initial_funds
        self.funds = initial_funds
        self.current_date = start_date
        self.holdings = defaultdict(int)
        
    def execute_transaction(self, transaction):
        if transaction.isBuy():
            self.buy_stock(transaction.stock, transaction.amount, transaction.date) 
        elif transaction.isSell():
            self.sell_stock(transaction.stock, transaction.amount, transaction.date)
    
    def buy_stock(self, stock, amt, date):
        '''
        Buy a specific amount of shares.
        '''
        price = stock.get_price_at_date(date)
        transaction_cost = price * amt
        if transaction_cost > self.funds:
            print 'Warning: tried to buy stock with inadequate funds! Transaction cancelled!'
            return
        self.holdings[stock] += amt
        self.funds -= transaction_cost
        
    def buy_stock_cash(self, stock, cash_amt, date):
        '''
        Buy the maximum amount of shares of a given stock that the amount of cash will allow.
        '''
        price = stock.get_price_at_date(date)
        num_shares = int(cash_amt / price)
        transaction_cost = price * num_shares
        if transaction_cost > self.funds:
            print 'Warning: tried to buy stock with inadequate funds! Transaction cancelled!'
            return
        self.holdings[stock] += num_shares
        self.funds -= transaction_cost
        
    def sell_stock(self, stock, amt, date):
        shares_held = self.holdings[stock]
        if shares_held < amt:
            print "Warning: tried to sell more shares than were held! Had %d sold %d. Transaction cancelled!" % (shares_held, amt)
            return
        self.holdings[stock] -= amt
        price = stock.get_price_at_date(date)
        self.funds += price * amt
        
    def profit(self):
        return self.funds - self.initial_funds
