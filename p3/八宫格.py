# coding=utf-8
'''
Created on 2015年8月25日

@author: Administrator
'''
import itertools

coordinates = []
for x in range(1, 4):
    for y in range(1, 5):
        coordinates.append((x, y))

print coordinates


print len(list(itertools.permutations([1, 2, 3, 4, 5, 6, 7, 8], 8)))
