# coding=utf-8
'''
Created on 2015年7月7日

@author: Administrator
'''


def newf():
    def he(x, y):
        return x + y
    return he

abc = newf()
print abc(19, 10)

astring = 'this is a global variable'


'''
def foo():
    print locals()
print globals()
'''
def boo():
    astring = 12313
    print locals()
    print astring

boo()
print astring



class ABC():
    pass

print issubclass(ABC, object)
print issubclass(boo.__class__, object)