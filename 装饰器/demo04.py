# coding=utf-8
'''
Created on 2015年7月7日
装饰器其实就是一个闭包,把一个函数当作参数然后返回一个替代版函数
@author: Administrator
'''


def deco(func):
    def inner():
        print 'before myfunc() called'
        func()
        print 'after myfunc() called'
    return inner


@deco
def myfunc():
    print 'myfunc() called'


myfunc()
myfunc()

'''
下面这种写法为什么只有第一次,装饰函数的方法调用了
'''


def wrapper(func):
    print 'before'
    func()
    print 'after'
    return func


@wrapper
def yuan():
    print 'yuan called'

yuan()
yuan()