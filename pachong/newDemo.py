# coding=utf-8
'''
Created on 2015年4月14日

@author: Administrator
'''
import urllib2


try:
    print urllib2.urlopen('http://odds.500.com/fenxi/ouzhi-452231.shtml?ctype=2')
except urllib2.HTTPError, e:
    print e.code
    print e.msg
    print e.headers
    print e.fp.read()
