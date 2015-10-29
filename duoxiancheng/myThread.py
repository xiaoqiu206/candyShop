# coding=utf-8
'''
Created on 2015年5月22日
让Thread的子类更加通用,把子类单独放到一个模块中,并加上一个getResult()函数,用以返回函数运行的结果
@author: Administrator
'''
import threading
from time import ctime


class MyThread(threading.Thread):

    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.name = name

    def getResult(self):
        return self.res

    def run(self):
        print 'starting', self.name, 'at:', ctime()
        self.res = apply(self.func, self.args)
        print self.name, 'finished at:', ctime()
