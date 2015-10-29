#coding=utf-8
'''
Created on 2015年5月31日

@author: Administrator
'''
from multiprocessing import Process, Manager

def f(adict, alist):
    adict[1] = '1'
    adict['2'] = 2
    adict[0.25] = None
    alist.reverse()

if __name__ == '__main__':
    manager = Manager()

    adict = manager.dict()
    alist = manager.list(range(10))

    p = Process(target=f, args=(adict, alist))
    p.start()
    p.join()

    print adict
    print alist