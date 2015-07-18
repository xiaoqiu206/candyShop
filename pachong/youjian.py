# coding=utf-8
'''
Created on 2015年7月10日

@author: Administrator
'''
from poplib import POP3
import base64


p = POP3('pop.163.com')
p.user('xiaoqiu206')
p.pass_('kono766191')
rsp, msg, siz = p.retr(17)
for eachline in msg:
    print eachline


print base64.decodestring('5rWL6K+V5YaF5a65LOaXoOmcgOWbnuWkjQ==')