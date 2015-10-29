#coding=utf-8
'''
Created on 2015年5月23日
每个程序员1小时内必须解决的5个编程问题
http://developer.51cto.com/art/201505/476097.htm
1.使用for循环、while循环和递归写出3个函数来计算给定数列的总和。
@author: Administrator
'''
from time import ctime

def usefor(numlist):
    sum = 0
    for num in numlist:
        sum += num
    return sum


def usewhile(numlist):
    sum = 0
    n = 0
    length = len(numlist)
    while n < length:
        sum = sum + numlist[n]
        n += 1
    return sum

def userecursive(numlist):
    pass

if __name__ == '__main__':
    numlist = [x*x for x in range(1,20000)]
    print ctime()
    print usefor(numlist)
    print ctime()
    print usewhile(numlist)
    print ctime()
    print sum(numlist)
    print ctime()