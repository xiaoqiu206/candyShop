# coding=utf-8
'''
Created on 2015年5月29日
一个进程里最多有多少个线程?
@author: Administrator
'''
from time import sleep
import threading


class MyThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print '  ',
        sleep(100)


def main():
    nthreads = []
    for _ in range(5000):
        myThread = MyThread()
        nthreads.append(myThread)

    for k, nthread in enumerate(nthreads):
        nthread.start()
        print k

    for nthread in nthreads:
        nthread.join()

if __name__ == '__main__':
    main()
