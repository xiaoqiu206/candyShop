# coding=utf-8
'''
Created on 2015年11月4日

@author: xiaoq
'''
import time

t1 = time.time()

print sum(xrange(100000000))
t2 = time.time()

print t2 - t1