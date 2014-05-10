'''
Created on Apr 20, 2014

@author: Lucas
'''
from random import choice

def read_fortune_500_symbols(file_path):
    with open(file_path) as f:
        lines = f.readlines()
        stocks = map(lambda x: x.strip(), lines)
        return stocks
    
_f500_ls = read_fortune_500_symbols('../resources/fortune500Symbols.txt')
fortune_500_tickers = set(_f500_ls)

def random_ticker():
    return choice(_f500_ls)