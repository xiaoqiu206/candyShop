# coding=utf-8
'''
Created on 2015年11月10日

@author: xiaoq
'''
from gevent import monkey
monkey.patch_all()
import gevent
from gevent.queue import Queue

q = Queue()


def producer():
    gevent.sleep(0.3)
    q.put(1)
    print 'put 1'


def customer():
    flag = True
    while flag:
        if not q.empty():
            print q.get()
            gevent.sleep(0.0001)


gs = [gevent.spawn(producer)] * 5
g2 = gevent.spawn(customer)

gevent.joinall(gs)

print 'done'
