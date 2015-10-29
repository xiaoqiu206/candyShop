# coding=utf-8
'''
Created on 2015年7月2日

@author: Administrator
'''
import urllib

import gevent
from gevent import monkey
monkey.patch_all()


def foo():
    print urllib.urlopen('http://www.qq.com').read().__len__(), 1
    print urllib.urlopen('http://www.sina.com').read().__len__(), 2
    print urllib.urlopen('http://www.baidu.com').read().__len__(), 3
    

def bar():
    print urllib.urlopen('http://www.51cto.com').read().__len__(), 4
    print urllib.urlopen('http://www.csdn.com').read().__len__(), 5
    print urllib.urlopen('http://www.163.com').read().__len__(), 6


def main():
    gevent.joinall([
        gevent.spawn(foo),
        gevent.spawn(bar)

    ])


if __name__ == '__main__':
    main()
