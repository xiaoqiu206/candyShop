# coding=utf-8
'''
Created on 2015年6月26日
异步发送http请求
@author: Administrator
'''
from tornado.httpclient import AsyncHTTPClient
from tornado import gen
import tornado
import time


def main():
    urls = (
        'http://www.sina.com',
        'http://www.baidu.com',
        'http://www.163.com',
        'http://www.qq.com',
        'http://www.51cto.com',
        'http://www.csdn.com',
    )

    client.fetch('http://www.sina.com', f1)

    io = tornado.ioloop.IOLoop.instance()
    io.start()


def f1(response):
    print response.effective_url, len(response.body)
    print time.time()
    client.fetch('http://www.baidu.com', f2)


def f2(response):
    print response.effective_url, len(response.body)
    print time.time()
    client.fetch('http://www.51cto.com', f3)


def f3(response):
    print response.effective_url, len(response.body)
    print time.time()
    client.fetch('http://www.163.com', f4)


def f4(response):
    print response.effective_url, len(response.body)
    print time.time()
    client.fetch('http://www.csdn.com', f5)


def f5(response):
    print response.effective_url, len(response.body)
    print time.time()


if __name__ == '__main__':
    print time.time()
    client = AsyncHTTPClient()
    main()
