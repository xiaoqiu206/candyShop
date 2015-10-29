# coding=utf-8
'''
Created on 2015年6月21日

@author: Administrator
'''
from tornado.template import Template

# 在tornado应用之外使用python解释器导入模板模块尝试模板系统
# 此时,结果会被直接输出出来
content = Template('<h1>{{header}}</h1>')
print content.generate(header='Welcome!')


# 可以将任何Python表达式放在双大括号中
print Template('{{1+1}}').generate()
print Template("{{'scrambled eggs'[-4:]}}").generate()
print Template("{{ ', '.join([str(x*x) for x in range(10)]) }}").generate()
