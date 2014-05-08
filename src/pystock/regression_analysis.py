'''
Analyze the effectiveness of regression techniques.
Created on May 1, 2014

@author: lnunno
'''
import numpy as np
import matplotlib.pyplot as plt
from pystock.time_utils import timeframe
from pystock.Stock import Regression

def use_all_regression_methods(stock, n_prev, n_predict, start_date):
    '''
    Apply all regression methods to the given stock and save the results.
    '''
    tf = timeframe(start_date, n_prev, n_predict)
    for m in Regression.methods:
        r = stock.predict_prices(start_date, n_prev, n_predict, method=m,include_training_dates=True)
        stock.plot_price(tf[0], tf[-1]) # Ground truth.
        r.plot() 
        fig_title = '%s_%s_%04d-train_%04d-predict' % (stock.symbol, m, n_prev, n_predict)
        plt.savefig('../output/%s' % (fig_title))
        plt.close()
        
def apple_lin_regression_ex(stock_dict):
    '''
    A simple example to test out linear regression.
    '''
    symbol = 'AAPL'
    stock = stock_dict[symbol]
    max_dates = 180
    sample_range = np.linspace(5, max_dates, num=5).astype(int)
    n_predict = 45
    start_date = '2013-01-23'
    plt.figure()
    tf = timeframe(start_date, 180, n_predict)
    pr = stock.get_prices_range(tf[0], tf[-1])
    pr.plot(label='Actual price')
    for n_prev in sample_range:
        r = stock.predict_prices(start_date, n_prev, n_predict, method=Regression.LINEAR)
        r.plot(label='%d day window' % (n_prev))
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Linear regression window size comparison for AAPL')
    plt.legend()
    plt.savefig('../output/Linear_regression_comparison_%d_day_prediction' % (n_predict))
    
def apple_svr_regr(stock_dict):
    symbol = 'AAPL'
    stock = stock_dict[symbol]
    max_dates = 2500
    sample_range = np.linspace(5, max_dates, num=4).astype(int)
    n_predict = 45
    start_date = '2013-01-23'
    plt.figure()
    tf = timeframe(start_date, 2500, n_predict)
    pr = stock.get_prices_range(tf[0], tf[-1])
    pr.plot(label='Actual price')
    for n_prev in sample_range:
        r = stock.predict_prices(start_date, n_prev, n_predict, method=Regression.SVR_RBF)
        r.plot(label='%d day window' % (n_prev))
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('SVR window size comparison for AAPL')
    plt.legend()
    plt.savefig('../output/SVR_comparison_%d_day_prediction' % (n_predict))

def apple_all_ex(stock_dict):
    '''
    A simple example to test out linear regression.
    '''
    symbol = 'AAPL'
    stock = stock_dict[symbol]
    max_dates = 180
    sample_range = np.linspace(5, max_dates, num=5).astype(int)
    n_predict = 45
    start_date = '2007-01-23'
    for n_prev in sample_range:
        use_all_regression_methods(stock, n_prev, n_predict, start_date)
    
def regression_analysis(stock_dict):
    apple_all_ex(stock_dict)
    apple_svr_regr(stock_dict)
