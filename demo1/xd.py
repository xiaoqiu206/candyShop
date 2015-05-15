# coding=utf-8
'''
Created on 2015锟斤拷5锟斤拷12锟斤拷

@author: Administrator
'''
import thread
import urllib2
urllib.urlopen
count = 0


def pa(n):
    print count

while 1:
    thread.start_new_thread(pa, (1,))
    count += 1

urllib2.urlopen(url, data, timeout, cafile, capath, cadefault, context)