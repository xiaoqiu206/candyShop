# coding=utf-8
'''
Created on 2015年5月21日
使用线程和锁,
如果线程执行的时间不能事先确定的话,可能造成主线程过早或过晚退出,所以要用锁
使用thread模块只是为了演示如何进行多线程,
正式的多线程程序应该使用更高级别的模块threading
@author: Administrator
'''
import thread
from time import sleep, ctime

loops = [2, 4]


def loop(nloop, nsec, lock):
    print 'start loop', nloop, 'at:', ctime()
    sleep(nsec)
    print 'loop', nloop, 'done at:', ctime()
    lock.release()


def main():
    print 'start at:', ctime()
    locks = []
    nloops = range(len(loops))

    # 创建2个锁,放到locks里
    for i in nloops:
        lock = thread.allocate_lock()
        lock.acquire()
        locks.append(lock)

    # 创建2个线程,每个线程分配一个锁
    for i in nloops:
        thread.start_new_thread(loop, (i, loops[i], locks[i]))

    # 这句话很重要,在线程结束的时候,线程要自己去做解锁操作,
    # 这个循环只是坐在这里一直等(达到暂停主线程的目的)
    # 知道2个锁都被解锁为止才继续运行,由于要顺序检查每一个锁,所以可能会要更长的时间
    # 等待运行时间长且放在前面的线程,当这些线程的锁释放后,后面的锁可能早就释放了(表示对应的线程已经运行完了)
    for i in nloops:
        while locks[i].locked():
            pass

    print 'all Done at:', ctime()


if __name__ == '__main__':
    main()
