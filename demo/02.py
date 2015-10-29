# coding=utf-8
'''
Created on 2015年10月22日

@author: xiaoq
'''
a = {'this': 7, 'is': 7, 'the': 7, 'first': 1, 'second': 1, 'third': 1,
     'forth': 1, 'fifth': 1, 'sixth': 1, 'seventh': 1, 'line': 3}
b = {}
for k, v in a.items():
    if v in b:
        b.setdefault(v, b.get(v).append(k))
    else:
        b.setdefault(v, [k])

print b
b.update({1:3})
print b