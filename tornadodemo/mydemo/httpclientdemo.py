# coding=utf-8
'''
Created on 2015年6月26日
异步发送http请求
@author: Administrator
'''
import tornado.ioloop
from tornado.httpclient import AsyncHTTPClient
import time


ioloop = tornado.ioloop.IOLoop.instance()
num = 6


def f(response):
    print response.body.__len__(), response.effective_url
    print time.time()

def handle_request(response):
    '当有response的时候的回调方法'
    if response.error:
        print 'Error', response.error

    else:
        print len(response.body), response.effective_url
    global num
    global ioloop
    num = num - 1
    if num == 3:
        http_client.fetch('http://www.aliyun.com', f)

    if num == 0:
        global t1
        ioloop.stop()


urllist = (
    'http://www.sina.com',
    'http://www.baidu.com',
    'http://www.163.com',
    'http://www.qq.com',
    'http://www.51cto.com',
    'http://www.csdn.com',
)
http_client = AsyncHTTPClient()

for url in urllist:
    http_client.fetch(url, f)

t1 = time.time()
ioloop.start()
