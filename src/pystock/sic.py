'''
Created on Apr 12, 2014

@author: Lucas
'''
import re

class Industry(object):

    def __init__(self, code, abbrv, name):
        self.code = code
        self.abbrv = abbrv
        self.name = name
        self.sectors = []
    
    def add_sector(self, sector):
        self.sectors.append(sector)
    
    def __repr__(self, *args, **kwargs):
        return self.sectors.__repr__()
        
class Sector(object):
    
    def __init__(self, range_start, range_end, name):
        self.range_start = range_start
        self.range_end = range_end
        self.name = name 
    
    def __repr__(self, *args, **kwargs):
        return '%s %d-%d' % (self.name,self.range_start,self.range_end)
    
    def in_sector(self,code):
        return self.range_start <= code <= self.range_end
        
def load_sic_code_file(file_path):
    # Groups: number, abbreviation, full name
    industry_pattern = re.compile('\s*(\d+)\s+(\w+)\s+([^\n]+)')
    range_pattern = re.compile('\s*(\d+)-(\d+)\s+([^\n]+)')
    industry_ls = []
    current_industry = None
    with open(file_path) as f:
        for line in f:
            industry_match = re.match(industry_pattern, line)
            sector_match = re.match(range_pattern, line)
            if industry_match:
                if current_industry:
                    industry_ls.append(current_industry)
                (code, abbrv, name) = industry_match.groups()
                current_industry = Industry(code, abbrv, name)
            elif sector_match:
                if not current_industry:
                    raise ValueError('Mismatching industry and sector values orphan sector %s' % (sector_match.groups().__repr__()))
                else:
                    (start, end, name) = sector_match.groups()
                    sector = Sector(int(start), int(end), name)
                    current_industry.add_sector(sector)
    return industry_ls
        
