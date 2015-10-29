# coding=utf-8
'''
Created on 2015年7月5日
发送邮件
@author: Administrator
'''
from poplib import POP3
import time
import re

p = POP3('pop.qq.com')
p.user('308227746')
p.pass_('gfdsa308227746')

# while 1:
#     print p.stat()[0] + 1000000000000
#     time.sleep(3)
rsp, msg, siz = p.retr(p.stat()[0] - 3)
url = None
for eachline in msg:
    if re.match(r'https://\S+',eachline):
        url = eachline
        print url
