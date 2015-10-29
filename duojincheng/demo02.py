# coding=utf-8
'''
Created on 2015年5月31日

@author: Administrator
'''
from multiprocessing import Process


def f(name):
    print 'hello', name

if __name__ == '__main__':
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()
