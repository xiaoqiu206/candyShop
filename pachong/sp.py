# coding=utf-8
'''
Created on 2015年4月16日

@author: Administrator
'''
from splinter import Browser
import time


b1 = Browser()
time.sleep(2)
b1.visit("http://www.baidu.com")
b1.find_by_id('kw')[0].fill(u'成都')
time.sleep(5)
b1.find_by_id('kw')[0].fill(u'成都哪里')
time.sleep(5)
b1.find_by_id('kw')[0].fill(u'成都哪里美女多')
time.sleep(5)
b1.find_by_id('su')[0].click()



