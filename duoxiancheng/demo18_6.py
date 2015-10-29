# coding=utf-8
'''
Created on 2015年5月21日
子类化Thread类,而不是创建他的实例
@author: Administrator
'''
import threading
from time import sleep, ctime

loops = [2, 4]


class MyThread(threading.Thread):

    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args

    def run(self):
        apply(self.func, self.args)

def loop(nloop, nsec):
    print 'start loop,', nloop, 'at:', ctime()
    sleep(nsec)

def main():
    print 'starting at:', ctime()
    threads = []
    nloops = range(len(loops))

    for i in nloops:
        t = MyThread(loop, (i, loops[i]), loop.__name__)
        threads.append(t)

    for i in nloops:
        threads[i].start()

    for i in nloops:
        threads[i].join()

    print 'all Done at:', ctime()

if __name__ == '__main__':
    main()