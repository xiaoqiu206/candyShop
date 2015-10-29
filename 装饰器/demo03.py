# coding=utf-8
'''
Created on 2015年7月7日

@author: Administrator
'''


def outer(x):
    def inner():
        print x
    return inner


print1 = outer(1)
print2 = outer(2)

print1()
print2()
