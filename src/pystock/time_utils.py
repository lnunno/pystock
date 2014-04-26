'''
Created on Apr 26, 2014

@author: lnunno
'''
import numpy as np
import pandas as pd

def next_n_business_days(start_date, n, include_start=False):
    '''
    @return: A list of the next n valid business days.
    '''
    dates = []
    if include_start and np.is_busday(start_date):
        dates.append(np.datetime64(start_date))
    curr_date = start_date
    for _ in range(n):
        curr_date = next_business_day(curr_date)
        dates.append(curr_date)
    return dates

def prev_n_business_days(start_date, n, include_start=False):
    '''
    @return: A list of the previous n valid business days.
    '''
    dates = []
    if include_start and np.is_busday(start_date):
        dates.append(np.datetime64(start_date))
    curr_date = start_date
    for _ in range(n):
        curr_date = prev_business_day(curr_date)
        dates.append(curr_date)
    return dates

def timeframe(start_date, num_previous_days, num_succ_days):
    '''
    NOTE: The start_date will only be included if it is a valid business day.
    
    @return: A list of business days prior, including, and after the start_date.  
    '''
    pds = prev_n_business_days(start_date, num_previous_days, include_start=False)
    pds.reverse()
    nds = next_n_business_days(start_date, num_succ_days, include_start=True)
    return pds + nds

def prev_business_day(day):
    '''
    Roll the clock backward one business day.
    '''
    return np.busday_offset(day, -1, roll='backward')

def next_business_day(day):
        '''
        Roll the clock forward one business day.
        
        See the numpy example:
        >>> # First business day after a date
        ... np.busday_offset('2011-03-20', 1, roll='backward')
        numpy.datetime64('2011-03-21','D')
        '''
        d = np.busday_offset(day, 1, roll='backward')
        return d
    
def datetime64_to_ordinal(dt64):
    return float(pd.to_datetime(dt64).toordinal())

def datetime64_to_ordinal_arr(dt64_ls):
    return np.array([datetime64_to_ordinal(dt64) for dt64 in dt64_ls])
