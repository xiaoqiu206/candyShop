# coding=utf-8
'''
Created on 2015年11月4日

@author: xiaoq
'''
import hashlib
in_file = open('in.txt', 'r')
out_file = open('out.txt', 'w')
m = hashlib.md5()

for line in in_file:
    p = line.index(',')
    t1 = line[0:p]
    t2 = line[p:]
    m.update(t1.encode("gb2312"))
    out_file.write(m.hexdigest() + t2)
