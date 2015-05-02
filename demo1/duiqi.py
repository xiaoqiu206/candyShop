# coding=utf-8
'''
Created on 2015年4月29日
研究print对齐
@author: Administrator
'''

items = [
         ('data collector', 'ok'),
         ('prepar中', 'Warning'),
         ('output report', 'Fail')
         ]
fmt = '%20s %-9s'
print '\n'.join([fmt % x for x in items])