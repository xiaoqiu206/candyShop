# coding=utf-8
'''
Created on 2015年11月2日

@author: xiaoq
'''


def deco(func):
    def _deco():
        print 'before called.'
        func()
        print 'after called.'
    return _deco


@deco
def myfunc():
    print 'called'


myfunc()