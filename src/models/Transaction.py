'''
Created on Feb 17, 2014

@author: lnunno
'''

class Transaction(object):
    '''
    classdocs
    '''

    buy = 'BUY'
    sell = 'SELL'

    def __init__(self, stock, transaction_type, amount, date):
        '''
        Constructor
        '''
        self.stock = stock
        self.transaction_type = transaction_type
        self.amount = amount
        self.date = date
        
    def isBuy(self):
        return self.transaction_type == self.buy
    
    def isSell(self):
        return self.transaction_type == self.sell
