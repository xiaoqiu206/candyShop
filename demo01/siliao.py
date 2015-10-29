# coding=utf-8
'''
Created on 2015年5月26日
把饲料的对错题目,筛选
@author: Administrator
'''
from .config import ABC

print ABC

dui_count = 0
cuo_count = 0
with open('panduan.txt') as f1:
    for line in f1:
        if line.find('(对)') > -1:
            dui_count += 1
            continue
        if line.find('(错)') > -1:
            cuo_count += 1
            # print line
            print line,
print dui_count,cuo_count
