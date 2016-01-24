# coding=utf-8
'''
Created on 2016年1月20日

@author: xiaoq
'''
from random import randrange
import functools
from time import time

print map(lambda a, b, c: a + b + c, [1, 2], [3, 4], [5, 6])

seq = [randrange(1000**1000) for i in range(1000)]


def timeit(func):
    def inner():
        t1 = time()
        ret = func()
        t2 = time()
        print '%s cost %s sec.' % (func.__name__, t2 - t1)
        return ret
    return inner


@timeit
def f1():
    dd = float('inf')
    for x in seq:
        for y in seq:
            if x == y:
                continue
            d = abs(x - y)
            if d < dd:
                xx, yy, dd = x, y, d
    print xx, yy


@timeit
def f2():
    seq.sort()
    dd = float('inf')
    for i in range(len(seq) - 1):
        x, y = seq[i], seq[i + 1]
        if x == y:
            continue
        d = abs(x - y)
        xx, yy, dd = x, y, d
    print xx, yy


f1()
f2()
