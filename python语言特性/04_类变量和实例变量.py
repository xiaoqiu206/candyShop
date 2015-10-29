# coding=utf-8
'''
Created on 2015年10月14日
类变量就是供类使用的变量,实例变量就是供实例使用的.
这里p1.name="bbb"是实例调用了类变量,这其实和上面第一个问题一样,就是函数传参的问题,p1.name一开始是指向的类变量name="aaa",
但是在实例的作用域里把类变量的引用改变了,就变成了一个实例变量,self.name不再引用Person的类变量name了.

但是如果类变量是可变的,那么更改实例变量也会更改类变量
详细情况看书
@author: xiaoq
'''


class Person:
    name = "aaa"


class A():
    name = {'1': 1}

a1 = A()
print a1.name
a1.name['2'] = 2
print A.name
b1 = A()
print b1.name

p1 = Person()

print dir(p1)
print p1.__dict__
p2 = Person()
p1.name = "bbb"
p2.name = "ccc"
print p1.__dict__

print p1.name
print p2.name
print Person.name
del p1.name
print p1.name
