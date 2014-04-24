'''
Created on Feb 16, 2014

@author: lnunno
'''
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from sklearn.linear_model import SGDRegressor

class Stock(object):
    '''
    Model of a Stock.
    
    Internally, this is just a specialized view of the master DataFrame which holds all the stock data.
    
    This object also provides equivalence and hashing behavior 
    so that it can be stored in hashed data structures like dictionaries.
    In these cases, the symbol (ticker) is compared and used as the hash.
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
    
    def get_prices_range(self, start_date, end_date):
        '''
        Get the stock prices between start_date and end_date.
        @param start_date: str The beginning date to get price info.
        @param end_date: str The ending date to get price info.
        '''
        return self.get_price_time_series()[start_date:end_date]
    
    def get_price_at_date(self, date):
        return self.get_price_time_series()[date]
    
    def _iso_to_date(self, s):
        return datetime.strptime(s, '%Y-%m-%d').date()
    
    def plot_price(self, start_date, end_date, show=False, save_path=''):
        price_ts = self.get_prices_range(start_date, end_date)
        plt.figure()
        plot = price_ts.plot()
        plt.xlabel('Time')
        plt.ylabel('Price')
        plt.title('Price for %s from %s to %s' % (self.symbol, start_date, end_date))
        if show:
            plt.show(plot)
        elif save_path:
            plt.savefig(plot)
        return plot
    
    def predict_price_at(self, start_date, end_date, predict_dates, method='SGD'):
        '''
        @param start_date: Date to use as beginning of training data.
        @param end_date: Date to use as end of training data.
        @param predict_dates: Dates to predict prices of.
        '''
        pr = self.get_prices_range(start_date, end_date)
        dates = pr.index.values
        prices = pr.values
        X = dates.reshape(dates.shape[0], 1)  # Have to reshape into a 2d array from a 1d array.
        y = prices.values
        
        # Train using the training X and y data.
        if method == 'SGD':
            regressor = SGDRegressor()
        else:
            raise ValueError('Unrecognized regression method %s' % (method))
        regressor.fit(X, y)
        predictions = regressor.predict(predict_dates)
        return predictions
        
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
