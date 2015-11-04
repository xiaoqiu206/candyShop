# coding=utf-8
'''
Created on 2015年5月18日
多线程demo1,thread模块的使用,不使用线程的情况下,顺序执行
@author: Administrator
'''
from time import ctime, sleep


def loop0():
    print 'start loop 0 at:', ctime()
    sleep(4)
    print 'loop 0 done at:', ctime()


def loop1():
    print 'start loop1 at:', ctime()
    sleep(2)
    print 'loop1 done at:', ctime()


def main():
    print 'starting at:', ctime()
    loop0()
    loop1()


if __name__ == '__main__':
    main()
