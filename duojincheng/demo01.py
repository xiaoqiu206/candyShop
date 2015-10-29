# coding=utf-8
'''
Created on 2015年5月31日

@author: Administrator
'''
from multiprocessing import Pool


def f(x):
    return x * x

if __name__ == '__main__':
    p = Pool(5)
    print p.map(f, [1, 2, 3])
