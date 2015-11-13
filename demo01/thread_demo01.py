# coding=utf-8
'''
Created on 2015年11月11日

@author: xiaoq
'''
from threading import Thread
from multiprocessing import Process


def test():
    x = 1
    while True:
        x += 1

if __name__ == "__main__":
    for _ in range(2):
        t = Process(target=test)
        t.start()
