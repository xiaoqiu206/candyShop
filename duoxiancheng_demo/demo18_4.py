# coding=utf-8
'''
Created on 2015年5月21日
使用threading模块
@author: Administrator
'''
import threading
from time import sleep, ctime

loops = [4, 2]


def loop(nloop, nsec):
    print 'start loop', nloop, 'at:', ctime()
    sleep(nsec)
    print 'loop', nloop, 'done at:', ctime()


def main():
    print 'start at:', ctime()
    threads = []
    nloops = range(len(loops))

    for i in nloops:
        t = threading.Thread(target=loop, args=(i, loops[i]))
        threads.append(t)

    for i in nloops:
        threads[i].start()
        
    # join会等到线程结束,或者在给了timeout参数的时候
    # 等到超时为止
    for i in nloops:
        threads[i].join()

    print 'all Done at:', ctime()

if __name__ == '__main__':
    main()
