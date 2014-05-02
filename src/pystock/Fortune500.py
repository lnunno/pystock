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
    
fortune_500_tickers = set(read_fortune_500_symbols('../resources/fortune500Symbols.txt'))

def random_ticker():
    return choice(fortune_500_tickers)