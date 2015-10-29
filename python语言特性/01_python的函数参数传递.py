#coding=utf-8
'''
Created on 2015年10月9日

@author: xiaoq
'''
a = 1
def afunc(a):
    a = 2
afunc(a)
print a


b = []
def bfunc(b):
    b.append(1)
bfunc(b)
print b

'''
所有的变量都可以理解是内存中一个对象的“引用”，或者，也可以看似c中void*的感觉。
这里记住的是类型是属于对象的，而不是变量。
而对象有两种,“可更改”（mutable）与“不可更改”（immutable）对象。在python中，strings, tuples, 和numbers是不可更改的对象，
而list,dict等则是可以修改的对象。(这就是这个问题的重点)
当一个引用传递给函数的时候,函数自动复制一份引用,这个函数里的引用和外边的引用没有半毛关系了.
所以第一个例子里函数把引用指向了一个不可变对象,当函数返回的时候,外面的引用没半毛感觉.
而第二个例子就不一样了,函数内的引用指向的是可变对象,对它的操作就和定位了指针地址一样,在内存里进行修改.
如果还不明白的话,这里有更好的解释: http://stackoverflow.com/questions/986006/how-do-i-pass-a-variable-by-reference
'''