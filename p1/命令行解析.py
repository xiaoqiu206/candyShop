# coding=utf-8
'''
Created on 2015年8月1日

@author: Administrator
'''
import sys
import getopt

opts, args = getopt.getopt(sys.argv[1:], 'd:f:h', ['days=', 'files=', 'help'])
print dict(opts)
print args
print __file__.decode('gbk')
print sys.argv[0].decode('gbk')