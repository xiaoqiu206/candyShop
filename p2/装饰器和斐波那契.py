# coding=utf-8
'''
Created on 2015年7月19日
用装饰器缓存斐波那契计算结果
@author: Administrator
'''


def cache(fib):
    temp = {}

    def _cache(n):
        if n not in temp:
            temp[n] = fib(n)
        return temp[n]
    return _cache


@cache
def fib(n):
    if n < 2:
        return n
    else:
        return fib(n - 1) + fib(n - 2)


if __name__ == '__main__':
    print fib(466)