# coding=utf-8
'''
Created on 2015年5月21日
使用thread的第一个例子
@author: Administrator
'''
import thread
from time import sleep, ctime


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
    thread.start_new_thread(loop1, ())
    thread.start_new_thread(loop0, ())
    '''
    这个sleep(6)的作用:如果主线程不停下来,会接着执行下一条语句,print 'all Done'
    然后,关闭运行着的loop0和loop1的2个线程,退出了,
    为什么是6秒?一个线程4秒,一个2秒,而且是并发执行,总时间应该不超过6秒,所以主线程等待6秒就应该结束了
    '''
    # sleep(6)
    '''
    如果把sleep(6)注释掉,starting at 和 all done at 都会打印出来,
    但是loop0和loop1不会执行,控制台会打印以下信息2次
    Unhandled exception in thread started by 
sys.excepthook is missing
错误应该是 python的主线程退出了，所以子线程启动不起来 (此结论来源于网络)
    '''
    print 'all Done at: ', ctime()


if __name__ == '__main__':
    '''
    尝试着改变sleep(6)的位置,看结果有什么不同,主线程是指的这整个程序,而不是某个方法
    当把sleep(6)改成1或2,会看到,loop0和loop1只有start,没有done
    '''
    main()
