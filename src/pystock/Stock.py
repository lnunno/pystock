'''
Created on Feb 16, 2014

@author: lnunno
'''
import pandas as pd
from datetime import datetime
from collections import OrderedDict
import matplotlib.pyplot as plt

class Stock(object):
    '''
    Model of a Stock.
    
    Internally, this is just a specialized view of the master DataFrame which holds all the stock data.
    '''

    def __init__(self, stock_data, symbol):
        '''
        
        @param symbol: The ticker or stock symbol for this stock. 
        '''
        idx = (stock_data.TICKER == symbol)
        self.data = stock_data.ix[idx]
        self.symbol = symbol
        
    def get_price_time_series(self):
        '''
        Get the stock's price time series data. 
        
        To get a range from the returned object you can, for instance, use partial string indexing which pandas will parse into the appropriate time index.
        
        Examples:
        tsd = stock.get_price_time_series()
        tsd['2011':'2013']  # Get the prices for the years 2011 - 2013
        tsd['10/31/2011':'12/31/2011'] # Daily prices for a 2 month period. 
        tsd['10/31/2011'] # Single day price 
         
        @see: http://pandas.pydata.org/pandas-docs/stable/timeseries.html#datetimeindex For a detailed description of how to use the DatetimeIndex.
        @return: A pandas Series object where the index is a DatetimeIndex and the values are the stock prices.
        '''
        date_index = pd.DatetimeIndex(self.data['date'])
        price_values = self.data['PRC'].values
        return pd.Series(price_values, index=date_index)
    
    def _iso_to_date(self, s):
        return datetime.strptime(s, '%Y-%m-%d').date()
    
    def plot_price(self, start_date, end_date):
        price_dict = self.get_prices_for_date_range(start_date, end_date)
        date_ls = [(self._iso_to_date(x), price) for x, price in price_dict.items()]
        date_ls.sort()
        print date_ls
    
    def __str__(self):
        return '%s' % (self.symbol)
    
    def __repr__(self):
        return self.__str__()
    
    def __hash__(self):
        return hash(self.symbol)
    
    def __eq__(self, other):
        return self.symbol == other.symbol
    
    def __ne__(self, other):
        return self.symbol != other.symbol
