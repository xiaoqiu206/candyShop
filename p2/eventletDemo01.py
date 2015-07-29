# coding=utf-8
'''
Created on 2015年7月24日
eventlet的demo
@author: Administrator
'''
import eventlet
from eventlet.green import urllib2
import time
urls = [
    'http://www.163.com',
    'http://www.aliyun.com',
    'http://www.qq.com',
    'http://www.sina.com',
    'http://www.baidu.com',
    'http://www.github.com',
    'http://www.51cto.com',
    'http://www.csdn.net'
]


def func(url):
    return urllib2.urlopen(url).read().__len__(), url
print time.time()
for url in urls:
    print func(url)
print time.time()


pool = eventlet.GreenPool()
for length, url in pool.imap(func, urls):
    print length, url
print time.time()
