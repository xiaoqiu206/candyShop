# coding=utf-8
'''
Created on 2015年5月31日

@author: Administrator
'''
from multiprocessing import Process, Queue


def f(q):
    q.put([42, None, 'hello'])

if __name__ == '__main__':
    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    print q.get() # prints "[42, None, 'hello']"
    p.join()