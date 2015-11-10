# coding=utf-8
'''
Created on 2015年11月8日

@author: xiaoq
'''


class Single(object):

    def __new__(cls, *args, **kws):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Single, cls).__new__(cls, *args, **kws)
        return cls._instance


class A(Single):
    pass


a1 = A()
a2 = A()

print id(a1), id(a2)
