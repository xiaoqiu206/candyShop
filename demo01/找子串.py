# coding=utf-8
'''
Created on 2015年11月1日
找出一个字符串中最大长度的从低到高排序的
@author: xiaoq
'''
import re

egs = 'azcbobobegghakl'
flags = ''
for k, v in enumerate(egs):
    if k == 0:
        continue
    if v >= egs[k - 1]:
        flags += '1'
    else:
        flags += '0'
ones = re.findall(r'1+', flags)
max_one = max(ones)
index = flags.find(max_one)
print egs[index:index + len(max_one) + 1]
