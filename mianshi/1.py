# coding=utf-8
"""
面试题目1,关于继承
"""


class Parent(object):
    x = 1


class Child1(Parent):
    pass


class Child2(Parent):
    pass

print Parent.x, Child1.x, Child2.x
Child1.x = 2
print Parent.x, Child1.x, Child2.x
Parent.x = 3
print Parent.x, Child1.x, Child2.x


fib = lambda x: x > 1 and fib(x - 1) + fib(x - 2) or 1
print fib(40)


def fib1(n):
    """
    斐波那契数列用循环实现
    :rtype : int
    """
    x, y = 1, 1
    while n:
        x, y, n = y, x + y, n - 1
    return x
print fib1(1000)
