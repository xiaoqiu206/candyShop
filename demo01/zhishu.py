# coding=utf-8
'''
Created on 2015年11月4日

@author: xiaoq
'''
import time


def a():
    for _ in range(90000):
        a = sum([2 ** x for x in range(65)])


def b():
    for _ in range(90000):
        a = sum(2 ** x for x in range(65))

t1 = time.time()
a()
t2 = time.time()
b()
t3 = time.time()

print t2 - t1, t3 - t2
