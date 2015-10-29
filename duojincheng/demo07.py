# coding=utf-8
'''
Created on 2015年5月31日

@author: Administrator
'''
from multiprocessing import Process, Value, Array


def f(n, a):
    n.value = 3.1415926
    for i in range(len(a)):
        a[i] = -a[i]

if __name__ == '__main__':
    num = Value('d', 0.0)
    arr = Array('i', range(10))

    p = Process(target=f, args=(num, arr))
    p.start()
    p.join()

    print num.value
    print arr[:]
