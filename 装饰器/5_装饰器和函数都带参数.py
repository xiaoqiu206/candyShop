# coding=utf-8
'''
Created on 2015年11月4日

@author: xiaoq
'''
import time
import functools


def log(module_name):
    """日志装饰器"""
    def _deco(func):
        @functools.wraps(func)
        def __deco(*args, **kwargs):
            t1 = time.time()
            ret = func(*args, **kwargs)
            t2 = time.time()
            print '%s %s(%s) use %s seconds' % (module_name, func.__name__, args, t2 - t1)
            return ret
        return __deco
    return _deco


@log('module1')
def add(x, y):
    """2个数相加"""
    time.sleep(1)
    return x + y

print add(1, 2)
print add.__name__, add.__doc__
