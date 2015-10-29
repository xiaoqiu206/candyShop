#coding=utf-8
'''
Created on 2015年5月31日

@author: Administrator
'''
from multiprocessing import Process,Lock

def f(alock,i):
    alock.acquire()
    print 'hello world', i
    alock.release()
    
if __name__ == '__main__':
    lock = Lock()
    
    for num in range(10):
        Process(target=f, args=(lock,num)).start()