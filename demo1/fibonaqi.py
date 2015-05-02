# coding=utf-8
'''
Created on 2015年5月2日
斐波那契数列
@author: Administrator
'''
import time
import sys


def now():
    return time.strftime('%H:%M:%S', time.localtime(time.time()))


def feibonaqi(n):
    if n in (0, 1):
        return 1
    else:
        return feibonaqi(n - 1) + feibonaqi(n - 2)


if __name__ == '__main__':
    print now()
    print feibonaqi(int(sys.argv[1]))
    print now()