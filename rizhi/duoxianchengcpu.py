# coding=utf-8
'''
Created on 2015年7月7日
多进程程序
@author: Administrator
'''
from multiprocessing import Pool
import os
import time
import random


def f(x):
    for i in range(100):
        print '%s --- %s' % (i, x)
        time.sleep(10)


def main():
    p = Pool(3)
    for i in range(11, 20):
        result = p.apply_async(f, (i,))
    p.close()
    p.join()
    if result.successful():
        print 'sucessful'

if __name__ == '__main__':
    main()
