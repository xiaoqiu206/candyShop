#coding=utf-8
'''
Created on 2015年10月16日
装饰器高级用法,在装饰器里传入参数
@author: xiaoq
'''
a = '''IPAddress   : 172.22.232.232
ScopeId     : 172.22.232.0
ClientId    : 66-55-44-33-22-11
Name        : test.pc.com
Description : test'''

b = a.split('\n')
line1 = ''
line2 = ''
print b
for each in b:
    
    line1 += each.split(':')[0].strip().ljust(20)
    line2 += each.split(':')[1].strip().ljust(20)
    
print line1, '\n', line2