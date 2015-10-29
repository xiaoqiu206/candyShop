# coding=utf-8
'''
Created on 2015年6月8日

@author: Administrator
'''


class AddrBookEntry(object):  # 类定义

    'address book entry class'

    def __init__(self, nm, ph):  # 定义构造器
        self.name = nm  # 设置name
        self.phone = ph  # 设置phone
        print 'Created instance for:', self.name

    def updatePhone(self, newph):  # 定义方法
        self.phone = newph
        print 'Updated phone# for:', self.name
