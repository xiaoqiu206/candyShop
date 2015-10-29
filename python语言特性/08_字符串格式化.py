#coding=utf-8
'''
Created on 2015年10月15日
字符串格式化:%和.format
.format在许多方面看起来更便利.对于%最烦人的是它无法同时传递一个变量和元组.
"hi there %s" % name 
可能没什么问题,但如果name恰好是(1,2,3),它将抛出一个TypeError异常.为了保证他总是正确的,你必须这样做:
"hi there %s" % (name,)  # 提供一个单元素的数组而不是一个参数
但是有点丑,.format就没有这些问题,唯一不使用.format的理由是:
1. 不知道它
2. 为了和python2.5兼容(例如logging建议使用%)
@author: xiaoq
'''
a = (1,2,3)
print "hi there {}".format(a)
print "{0}{1}{2}".format(1,2,3)
print "{0}{1}{0}".format(1,2,3)
