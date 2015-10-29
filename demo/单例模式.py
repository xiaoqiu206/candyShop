#coding=utf-8
'''
Created on 2015年10月20日

@author: xiaoq
'''
the_only = None

class A():
    pass

def get_a():
    global the_only
    if not the_only:
        the_only = A()
    return the_only

a1 = get_a()
a2 = get_a()

print id(a1), id(a2)