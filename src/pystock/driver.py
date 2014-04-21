'''
Created on Feb 16, 2014

@author: lnunno
'''
import numpy as np
import random
import os
import csv
import pandas as pd
from argparse import ArgumentParser
from numpy.random import normal
from math import ceil
from datetime import datetime
from pystock.sic import load_sic_code_file
from pystock.Fortune500 import fortune_500_tickers
from pystock.Stock import Stock

ticker_column = 4

def load_stock_csv_file(file_path):
    '''
    Load the given stock csv file and create a pandas DataFrame representation of the file.
    @return: A DataFrame of stock price data.
    '''
    abspath = os.path.abspath(file_path)
    print 'Loading %s...' % (abspath)
    def line_filterer(stock_file):
        for i, line in enumerate(stock_file):
            if i == 0:
                # Always yield the header.
                yield line
            # Parse the line as csv.
            reader = csv.reader([line])
            row = reader.next()
            if row[ticker_column] in fortune_500_tickers:
                yield line
            
    def date_conv(date_str):
        '''
        Convert the date from a string to a numpy datetime64 object.
        
        Expects the date to be formatted as %Y/%m/%d or else it will return None and print a warning.
        
        These are examples of valid input:
        '2004/01/30'
        '2014/02/23'
        etc.
        '''
        try:
            dt = datetime.strptime(date_str, '%Y/%m/%d')
            return np.datetime64(dt.strftime('%Y-%m-%d'))
        except ValueError:
            print "WARNING: Bad date string ", date_str
            return None
    with open(file_path) as stock_file:
        csv_data = np.genfromtxt(line_filterer(stock_file), delimiter=',', names=True,
                             dtype=('datetime64[D]', 'S10', 'S32', float, int, int, int, float),
                             usecols=('date', 'TICKER', 'COMNAM', 'PRC', 'VOL', 'SHROUT', 'SICCD', 'RET'),
                             converters={'date': date_conv}) 
    df = pd.DataFrame(csv_data)
    print 'Finished loading %s.' % (abspath)
    return df

def random_transaction(broker, date):
    flip = random.choice([True])
    base_amt = 10
    if flip:
        stock = random.choice(fortune_500_tickers)
        buy_amt = ceil(base_amt + base_amt * normal())
        broker.buy_stock(stock, buy_amt, date)
        return
    else:
        stock = random.choice(broker.holdings.keys())
        buy_amt = base_amt + base_amt * normal()
        broker.sell_stock(stock, buy_amt, date)
        return

def load_all_stock_files(root_dir, file_name_ls):
    '''
    Load all the stock data files from the given root directory. 
    @return: A concatenated master DataFrame containing the data from all the given csv files.
    '''
    data_frame_ls = []
    for file_name in file_name_ls:
        full_path = os.path.join(root_dir, file_name)
        df = load_stock_csv_file(full_path)
        data_frame_ls.append(df)
    full_df = pd.concat(data_frame_ls)
    return full_df 

def create_arg_parser():
    '''
    Create an argument for running the script with user defined values.
    '''
    parser = ArgumentParser()
    parser.add_argument('--loadStockDF', help='The path to a pickled DataFrame of stock data to load.', action='store', dest='load_pkl_path', default='')
    parser.add_argument('--saveStockDF', help='The path to save a pickled version of the stock data to.', action='store', dest='save_pkl_path', default='')
    return parser
    
def main():
    parser = create_arg_parser()
    args = parser.parse_args()
    load_pkl_path = args.load_pkl_path
    save_pkl_path = args.save_pkl_path
    if load_pkl_path:
        df = pd.read_pickle(load_pkl_path)
    else:
        file_name_ls = ['2005.csv', '2007.csv', '2009.csv', '2011.csv', '2013.csv']
        df = load_all_stock_files('F:/ml_data/FinanceDatasets', file_name_ls)
        if save_pkl_path:
            df.to_pickle(save_pkl_path)
    s = '../resources/Siccodes17.txt'
    industries = load_sic_code_file(s)
    stock_dict = {}
    for ticker in fortune_500_tickers:
        stock_dict[ticker] = Stock(df, ticker)
    print
    
if __name__ == '__main__':
    main()
    
