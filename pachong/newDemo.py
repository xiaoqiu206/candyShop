# coding=utf-8
'''
Created on 2015年4月14日

@author: Administrator
'''
import urllib2
import time


def now():
    return time.strftime('%H:%M:%S')

print now()


stocks = ['http://hq.sinajs.cn/list=sh' +
          str(x) for x in range(601008, 601555)]
with file('stock.txt', 'wb') as f:
    for stock in stocks:
        html = urllib2.urlopen(stock).read()
        f.write(html)

print now()
