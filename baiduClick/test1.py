# coding=utf-8
'''
Created on 2015年8月21日

@author: Administrator
'''
import socket
import gevent
import gevent.monkey

gevent.monkey.patch_all()


def check_proxy():
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(3)
    try:
        sk.connect(('127.0.0.1', 9999))
    except Exception:
        print 'no'
    sk.close()


def main():
    threads = []
    for _ in range(500):
        threads.append(gevent.spawn(check_proxy))
    gevent.joinall(threads)

if __name__ == '__main__':
    main()
