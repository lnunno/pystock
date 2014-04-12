'''
Created on Feb 16, 2014

@author: lnunno
'''
import numpy as np
from Stock import fortune_500_stocks
import random
from numpy.random import normal
from math import ceil
from datetime import datetime
from pystock.sic import load_sic_code_file

def load_stock_csv_file(file_path):
    def date_conv(date_str):
        dt = datetime.strptime(date_str,'%m/%d/%Y')
        return np.datetime64(dt.strftime('%Y-%m-%d'))
    csv_data = np.genfromtxt(file_path,delimiter=',',names = True, 
                             dtype=('datetime64[D]','S10','S32',float,int,int,int), 
                             usecols=('date','TICKER','COMNAM','PRC','VOL','SHROUT','SICCD'),
                             converters={'date': date_conv}) 
    return csv_data

def random_transaction(broker, date):
    flip = random.choice([True])
    base_amt = 10
    if flip:
        stock = random.choice(fortune_500_stocks)
        buy_amt = ceil(base_amt + base_amt * normal())
        broker.buy_stock(stock, buy_amt, date)
        return
    else:
        stock = random.choice(broker.holdings.keys())
        buy_amt = base_amt + base_amt * normal()
        broker.sell_stock(stock, buy_amt, date)
        return

if __name__ == '__main__':
    p = 'F:/ml_data/FinanceDatasets/energy_west.csv'
    s = '../resources/Siccodes17.txt'
    en_west = load_stock_csv_file(p)
    industries = load_sic_code_file(s)
    print
    
    
