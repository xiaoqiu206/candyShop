# coding=utf-8
'''
Created on 2015年11月2日
参数用(*args, **kwargs)自动适应变参合命名参数
@author: xiaoq
'''


def deco(func):
    def _deco(*args, **kwargs):
        print 'before called'
        ret = func(*args, **kwargs)
        print 'after called'
        return ret
    return _deco


@deco
def myfunc1(a, b):
    print 'myfunc1(%s, %s) called.' % (a, b)
    return a + b


@deco
def myfunc2(a, b, c):
    print 'myfunc2(%s, %s, %s) called.' % (a, b, c)
    return a + b + c

print myfunc1(1, 2)
print myfunc2(1, 2, 3)
