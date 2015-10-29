# coding=utf-8
'''
Created on 2015年7月7日

@author: Administrator
'''
def outer():
    x = 1
    y = 'abc'
    def inner():
        print x
        print y
    return inner


foo = outer()    
print foo.func_closure
foo()    

