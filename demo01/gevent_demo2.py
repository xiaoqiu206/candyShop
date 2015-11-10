# coding=utf-8
'''
Created on 2015年11月8日

@author: xiaoq
'''
from gevent import monkey
monkey.patch_all
import gevent
from gevent import Timeout
import time


def wait5():
    gevent.sleep(5)
    print 'has waited 5s'


def wait3():
    gevent.sleep(3)
    print 'has waited 3s'


def main():
    print 'start main()'
    Timeout(4).start()
    try:
        g1 = gevent.spawn(wait3)
        g2 = gevent.spawn(wait5)
        gevent.joinall([g1, g2])
    except Timeout:
        print 'timeout'
    print 'done'
    print g1.ready(), g2.ready()
    print g1.successful(), g2.successful()

if __name__ == '__main__':
    while 1:
        main()
        time.sleep(0.5)
