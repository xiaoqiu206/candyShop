# coding=utf-8
'''
Created on 2015年4月1日

@author: Administrator
'''
import hashlib

d5 = hashlib.md5('10197fyjnrgdgfsf464613131'.encode('utf-8')).hexdigest()

m = hashlib.md5()
m.update('10197fyjnrgdgfsf464613131')
print m.hexdigest()