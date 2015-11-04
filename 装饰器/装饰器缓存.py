# coding=utf-8
'''
Created on 2015年7月26日
用装饰器缓存斐波那契数列结果
@author: Administrator
'''


def cache(fn):
    _FIB_CACHE = {}

    def _cache(n):
        if n not in _FIB_CACHE:
            _FIB_CACHE[n] = fn(n)
        return _FIB_CACHE[n]
    return _cache


@cache
def fib(n):
    return fib(n - 1) + fib(n - 2) if n >= 2 else 1


print fib(400)

a = 29.08
b = 29.07
print a - b 
print a - b >= 0.009999999999999999999999999