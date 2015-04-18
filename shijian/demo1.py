# coding=utf-8
'''
Created on 2015年4月16日
小demo
@author: Administrator
'''
import re

s1 = 'afda[教务处]adfaf'
m = re.search(r'\[\S+\]',s1)
print m.group()
