#coding=utf-8
'''
Created on 2015年10月14日
python2.7中新加入的字典推导式
@author: xiaoq
'''
d = {key: value for (key, value) in enumerate([1 , 1, 3, 5])}
print d