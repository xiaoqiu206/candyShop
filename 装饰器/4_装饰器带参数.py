# coding=utf-8
'''
Created on 2015年11月2日

@author: xiaoq
'''


def deco(arg):
    def _deco(func):
        def __deco():
            print 'before %s called %s' % (func.__name__, arg)
            func()
            print 'after %s called %s' % (func.__name__, arg)
        return __deco
    return _deco


@deco('module1')
def myfunc1():
    print 'func1 called.'


@deco('module2')
def myfunc2():
    print 'func2 called.'

myfunc1()
myfunc2()
