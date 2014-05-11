'''
Analyze the effectiveness of regression techniques.
Created on May 1, 2014

@author: lnunno
'''
import numpy as np
import pandas as pd
from pystock.time_utils import timeframe, random_business_day
from pystock.Stock import Regression
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from sklearn.metrics.metrics import mean_absolute_error
from pystock.Fortune500 import random_ticker
from random import choice
from sklearn.utils.validation import check_arrays
from collections import defaultdict

def use_all_regression_methods(stock, n_prev, n_predict, start_date):
    '''
    Apply all regression methods to the given stock and save the results.
    '''
    tf = timeframe(start_date, n_prev, n_predict)
    for m in Regression.methods:
        r = stock.predict_prices(start_date, n_prev, n_predict, method=m,include_training_dates=True)
        stock.plot_price(tf[0], tf[-1]) # Ground truth.
        training_ts = r[:n_prev]
        testing_ts = r[n_prev:]
        training_ts.plot(label='Training data')
        testing_ts.plot(label='Testing data')
        plt.axis('auto')
        plt.legend()
#         r.plot() 
        fig_title = '%s_%s_%04d-train_%04d-predict' % (stock.symbol, m, n_prev, n_predict)
        plt.savefig('../output/%s' % (fig_title))
        plt.close()

def use_all_regression_methods_superimpose(stock, n_prev, n_predict, start_date):
    '''
    Apply all regression methods to the given stock and save the results.
    '''
    tf = timeframe(start_date, n_prev, n_predict)
    fig,ax = stock.plot_price(tf[0], tf[-1]) # Ground truth.
    error_ls = []
    for m in Regression.methods:
        r = stock.predict_prices(start_date, n_prev, n_predict, method=m,include_training_dates=True)
        training_ts = r[:n_prev]
        testing_ts = r[n_prev:]
        training_ts.plot(label=('%s training' % m) )
        testing_ts.plot(label=('%s testing' % m))
        yt = stock.prices[testing_ts.index.values]
        yw = yt[pd.notnull(yt.values)]
        y_pred = testing_ts[yw.index.values].values
        y_true = yw.values
        assert len(y_true) == len(y_pred)
        assert type(y_true) == type(y_pred)
        assert not np.any(np.isnan(y_true))
        assert not np.any(np.isnan(y_pred))
        error = calculate_error(y_true, y_pred)
        error_ls.append(error)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    fontP = FontProperties()
    fontP.set_size('small')
    plt.axis('auto')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5),
          fancybox=True, shadow=True,prop=fontP)
    fig_title = '%s_%04d-train_%04d-predict-superimposed' % (stock.symbol, n_prev, n_predict)
    plt.savefig('../output/%s' % (fig_title))
    plt.close()
    
    # Plot errors 
    plt.figure()
    index = np.arange(len(error_ls))
    colors = ['b','g','r']
    for i in index:
        plt.bar(i,error_ls[i],label=Regression.methods[i],color=colors[i])
    plt.xticks(index+0.4,Regression.methods)
    plt.title('Mean Absolute Error for %d training dates and %d testing dates' % (n_prev,n_predict))
    plt.legend()
    fig_title = '%s_error-%04d-%04d' % (stock.symbol, n_prev, n_predict)
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
    plt.legend(loc="upper left")
    plt.savefig('../output/Linear_regression_comparison_%d_day_prediction' % (n_predict))
    
def apple_svr_rbf_regr_window(stock_dict):
    symbol = 'AAPL'
    stock = stock_dict[symbol]
    max_dates = 180
    sample_range = np.linspace(5, max_dates, num=5).astype(int)
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
    plt.title('SVR RBF window size comparison for AAPL')
    plt.legend(loc="lower left")
    plt.savefig('../output/SVR_RBF_comparison_%d_day_prediction' % (n_predict))

def apple_svr_poly_regr_window(stock_dict):
    symbol = 'AAPL'
    stock = stock_dict[symbol]
    max_dates = 180
    sample_range = np.linspace(5, max_dates, num=5).astype(int)
    n_predict = 45
    start_date = '2013-01-23'
    plt.figure()
    tf = timeframe(start_date, 2500, n_predict)
    pr = stock.get_prices_range(tf[0], tf[-1])
    pr.plot(label='Actual price')
    for n_prev in sample_range:
        r = stock.predict_prices(start_date, n_prev, n_predict, method=Regression.SVR_POLY)
        r.plot(label='%d day window' % (n_prev))
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('SVR Poly window size comparison for AAPL')
    plt.legend(loc="lower left")
    plt.savefig('../output/SVR_POLY_comparison_%d_day_prediction' % (n_predict))

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
#         use_all_regression_methods(stock, n_prev, n_predict, start_date)
        use_all_regression_methods_superimpose(stock, n_prev, n_predict, start_date)

def calculate_error(y_true,y_pred):
    return mean_absolute_percentage_error(y_true,y_pred)

def mean_absolute_percentage_error(y_true, y_pred): 
    y_true, y_pred = check_arrays(y_true, y_pred)

    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

def random_stock_regression_sampling(stock_dict):
    train_days_arr = np.linspace(7,400,num=20).astype(int)
    test_days_arr =  np.array([2,5,7,30,60,90,180,365])
    num_tests = 150
    for test_num in test_days_arr:
        error_dict = defaultdict(list)
        for train_num in train_days_arr:
            for m in Regression.methods:
                ls = []
                i = num_tests
                while i > 0:
                    ticker = random_ticker()
                    stock = stock_dict[ticker]
                    while len(stock.prices.values) == 0:
                        # Get a stock with actual data.
                        ticker = random_ticker()
                        stock = stock_dict[ticker]
                    valid_days = np.array(stock.prices.index.values[train_num:-test_num],dtype='datetime64[D]') 
                    if len(valid_days) <= 0:
#                         print 'Warning %s did not have stock data for train=%d and test=%d' % (ticker,train_num,test_num)
                        continue
                    start_day = choice(valid_days)
                    try:
                        results = stock.predict_prices(start_day, train_num, test_num, method=m)
                        test_ts = stock.prices[results.index.values]
                    except ValueError:
#                         print 'Weird error on %s train=%d and test=%d' % (ticker,train_num,test_num)
                        continue
                    test_ts = test_ts[pd.notnull(test_ts)] # Filter null vals
                    y_pred = results[test_ts.index.values].values # Only get prediction dates where we have test values.
                    y_true = test_ts.values
                    try:
                        error = calculate_error(y_true, y_pred)
                    except ValueError:
                        continue
                    ls.append(error)
                    print 'Fine with ',ticker,train_num,test_num,m
                    i -= 1
                average_err = np.mean(ls)
                error_dict[m].append(average_err)
        plt.figure()
        for regr_method,mean_errors in error_dict.items():
            plt.plot(train_days_arr,mean_errors,label=regr_method)
            plt.xlabel('Training window size')
            plt.ylabel('Mean Abs % Error')
            plt.title('%d day Prediction with Varying Training Window Sizes' % (test_num))
        plt.legend(loc='upper center', ncol=3, fancybox=True)
        plt.savefig('../output/pred_error-%04d_days' % (test_num))
    
def regression_analysis(stock_dict):
#     apple_all_ex(stock_dict)
#     apple_lin_regression_ex(stock_dict)
#     apple_svr_poly_regr_window(stock_dict)
#     apple_svr_rbf_regr_window(stock_dict)
    random_stock_regression_sampling(stock_dict)
