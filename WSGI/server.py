# coding=utf-8
'''
Created on 2015年5月4日

@author: Administrator
'''
from wsgiref.simple_server import make_server
from app import application

# 创建一个服务器,ip为空,端口8000,处理函数是application
httpd = make_server('', 8000, application)
print 'Serving HTTP on port 8000...'
# 开始监听HTTP请求
httpd.serve_forever()