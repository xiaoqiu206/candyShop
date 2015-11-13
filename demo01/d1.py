# coding=utf-8
'''
Created on 2015年11月13日
角谷猜想
@author: xiaoq
'''
is_checked = []


def cache(func):
    def _wrap(n):
        if n in is_checked:
            return True
        else:
            ret = func(n)
            return ret
    return _wrap


@cache
def check(n):
    if n == 1:
        return True
    if n % 2 == 0:
        return check(n / 2)
    else:
        n = n * 3 + 1
        return check(n)

x = 2
while x < 9999999999999999:
    print x, check(x)
    x += 1