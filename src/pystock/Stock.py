'''
Created on Feb 16, 2014

@author: lnunno
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn import svm
from sklearn.preprocessing import scale
from pystock.time_utils import prev_n_business_days, next_n_business_days, \
    datetime64_to_ordinal_arr
from sklearn.linear_model.ridge import Ridge

class Regression(object):
    
    LINEAR = 'Linear'
    RIDGE = 'Ridge'
    SVR_RBF = 'SVR_RBF'
    SVR_POLY = 'SVR_POLY'
    
    
    methods = [
               LINEAR,
               SVR_RBF,
               SVR_POLY
               ]
    

class Stock(object):
    '''
    Model of a Stock.
    
    Internally, this is just a specialized view of the master DataFrame which holds all the stock data.
    
    This object also provides equivalence and hashing behavior 
    so that it can be stored in hashed data structures like dictionaries.
    In these cases, the symbol (ticker) is compared and used as the hash.
    
    @ivar prices: The price time series.
    '''

    def __init__(self, stock_data, symbol):
        '''
        @param symbol: The ticker or stock symbol for this stock. 
        '''
        idx = (stock_data.TICKER == symbol)
        self.data = stock_data.ix[idx]
        self.symbol = symbol
        self.prices = self.get_price_time_series()
        
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
        return self.prices[start_date:end_date]
    
    def get_prices_after(self, start_date, n):
        date_range = next_n_business_days(start_date, n, include_start=True)
        return self.get_prices_range(date_range[0], date_range[-1])
    
    def get_price_at_date(self, date):
        return self.prices[date]
    
    def plot_price(self, start_date, end_date, show=False, save_path=''):
        price_ts = self.get_prices_range(start_date, end_date)
        plt.figure()
        ax = plt.subplot(111)
        figure = price_ts.plot(label='Ground truth')
        ax.set_xlabel('Time')
        ax.set_ylabel('Price')
        ax.set_title('Price for %s from %s to %s' % (self.symbol, start_date, end_date))
        if show:
            plt.show(figure)
        elif save_path:
            plt.savefig(figure)
        return figure,ax
    
    def predict_prices(self,
                       predict_start,
                       num_previous_dates,
                       num_successive_dates,
                       include_training_dates=False,
                       method=Regression.LINEAR):
        '''
        Linear Regression (Linear): Standard linear regression.
        
        Support Vector Regression (SVR_RBF) is an extension of Support Vector Machines used to solve regression problems.
        An explanation and example of its usage are available here:
        http://scikit-learn.org/dev/modules/svm.html#regression
        http://scikit-learn.org/dev/auto_examples/svm/plot_svm_regression.html#example-svm-plot-svm-regression-py
        
        @param predict_start: string The date to start the prediction.
        @param num_previous_dates: int Number of dates to use prior to predict_start as the training data.
        @param num_successive_dates: int Number of dates to predict after predict_start.
        @param include_training_dates: bool Include the training dates in the predicted prices.
        @param method: Method used for regression. One of the Regression.methods values.
        
        @return: A Series with a DatetimeIndex with the dates and predicted prices.
        '''
        predict_dates = next_n_business_days(predict_start, num_successive_dates, include_start=True)
        training_dates = prev_n_business_days(predict_start, num_previous_dates, include_start=False)
        training_prices_series = self.get_prices_range(str(training_dates[-1]), str(training_dates[0]))
        training_date_index_ls = training_prices_series.index.values
        
        if include_training_dates:
            # Include training data in predictions.
            predict_dates = np.hstack((training_dates,predict_dates))
            
        td_ordinals = datetime64_to_ordinal_arr(training_date_index_ls)
        p = datetime64_to_ordinal_arr(predict_dates)
        
        
        # Have to reshape into a 2d array from a 1d array.
        p = p.reshape(p.shape[0], 1)
        X = td_ordinals.reshape(td_ordinals.shape[0], 1)
        
        # Normalize dates
        A = np.vstack((X, p))  # Have to stack to normalize training and test data as one.
        A = scale(A, axis=0)
        n = p.shape[0]
        X = A[:-n]
        p = A[-n:]
        
        y = training_prices_series.values
        
        if method == Regression.SVR_RBF:
            regressor = svm.SVR(kernel='rbf')
        elif method == Regression.SVR_POLY:
            regressor = svm.SVR(kernel='poly')
        elif method == Regression.RIDGE:
            regressor = Ridge()
        elif method == Regression.LINEAR:
            regressor = LinearRegression()
        else:
            raise ValueError('Unrecognized regression method %s' % (method))
        try:
            regressor.fit(X, y)  # Train using the training X and y data.
        except ValueError:
            raise ValueError('Issue fitting, re-throwing.')
        predictions = regressor.predict(p)
        index = pd.DatetimeIndex(predict_dates)
        series = pd.Series(predictions,index=index)
        return series
        
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
