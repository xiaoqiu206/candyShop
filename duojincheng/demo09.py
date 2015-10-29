# coding=utf-8
'''
Created on 2015年6月1日

@author: Administrator
'''
from multiprocessing import Pool


def f(x):
    return x * x

if __name__ == '__main__':
    pool = Pool(processes=4)  # start 4 worker processes
    result = pool.apply_async(f, [10])  # evalute "f(10)" asyncronously
    print result.get(timeout=1)  # prints "100" unless your computer is *very* slow
    print pool.map(f, range(10))  # prints "[0, 1, 4,..., 81]"
