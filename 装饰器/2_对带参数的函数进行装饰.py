# coding=utf-8
'''
Created on 2015年11月2日
内嵌包装函数的形参和返回值与原函数相同,
装饰函数返回内嵌包装函数对象
@author: xiaoq
'''


def deco(func):
    def _deco(a, b):
        print 'before called.'
        ret = func(a, b)
        print 'after called'
        return ret
    return _deco

@deco
def myfunc(a, b):
    print 'myfunc(%s, %s) called' % (a, b)
    return a + b

print myfunc(1, 2)
