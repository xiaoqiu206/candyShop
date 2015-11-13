# coding=utf-8
'''
Created on 2015年11月10日

@author: xiaoq
'''
import gevent
from gevent.pool import Group


def add(x):
    while 1:
        if x == 3:
            group.add(gevent.spawn(print_func, x))
            group.join()
        gevent.sleep(1)
        print x, 'add'
        x += 1


def delete(x):
    while 1:
        if x == 3:
            group.add(gevent.spawn(print_func, x))
            group.join()
        gevent.sleep(1)
        print x, 'delete'
        x -= 1


def print_func(x):
    while 1:
        gevent.sleep(1)
        print x, 'print'

group = Group()
group.add(gevent.spawn(add, 1))
group.add(gevent.spawn(delete, 10))
group.join()
group.add(gevent.spawn(print_func, 111))
group.join()
