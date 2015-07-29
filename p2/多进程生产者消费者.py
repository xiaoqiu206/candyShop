# coding=utf-8
'''
Created on 2015年7月25日
多进程的生产者,消费者
@author: Administrator
'''
import multiprocessing
import Queue
import time
from multiprocessing import Process, Pool


def f(x):
    time.sleep(5)
    return x * x

if __name__ == '__main__':
    q = Queue.Queue()
    print time.time()
    q.put(123)
    print time.time()
    print q.empty()
    print time.time()

    '''
    pool = Pool(processes=4)
    result = pool.apply_async(f, (10,))
    t1 = time.time()
    print result.get(timeout=10)
    t2 = time.time()
    print t2 - t1
    print pool.map(f, range(8))
    t3 = time.time()
    print t3 - t2
    '''
