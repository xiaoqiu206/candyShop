# coding=utf-8
'''
Created on 2015年8月7日

@author: Administrator
'''
import requests
import gevent
import gevent.monkey
gevent.monkey.patch_all()


def f1():
    r1 = requests.get('http://www.baidu.com')
    print r1.url
    r2 = requests.get('http://www.51cto.com')
    print r2.url
    r3 = requests.get('http://www.csdn.com')
    print r3.url


def f2():
    r1 = requests.get('http://www.sina.com')
    print r1.url
    r2 = requests.get('http://www.qq.com')
    print r2.url
    r3 = requests.get('http://www.163.com')
    print r3.url


def f3():
    r1 = requests.get('http://www.aliyun.com')
    print r1.url
    r2 = requests.get('http://www.taobao.com')
    print r2.url
    r3 = requests.get('http://www.jd.com')
    print r3.url


def main():
    gevent.joinall([
        gevent.spawn(f1),
        gevent.spawn(f2),
        gevent.spawn(f3),

    ])

if __name__ == '__main__':
    main()
