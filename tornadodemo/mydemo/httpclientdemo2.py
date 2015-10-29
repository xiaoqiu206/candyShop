# coding=utf-8
'''
Created on 2015年6月26日
异步发送http请求
@author: Administrator
'''
import tornado.ioloop
from tornado.httpclient import AsyncHTTPClient
import time
from tornado.gen import engine
import thread
from bs4 import BeautifulSoup as BS


@engine
def main1(client):
    response = yield client.fetch('http://www.baidu.com')
    print response.effective_url, BS(response.body).title.text
    response1 = yield client.fetch('http://www.qq.com')
    print response1.effective_url, BS(response1.body).title.text



@engine
def main2(client):
    response = yield client.fetch('http://www.sina.com.cn')
    print response.effective_url, BS(response.body).title.text
    response1 = yield client.fetch('http://www.163.com')
    print response1.effective_url, BS(response1.body).title.text


def m(ioloop):
    # ioloop = tornado.ioloop.IOLoop.instance()
    client = AsyncHTTPClient()
    main1(client)
    main2(client)
    t1 = time.time()
    ioloop.start()

if __name__ == '__main__':
    count = 1
    while 1:
        ioloop = tornado.ioloop.IOLoop.instance()
        thread.start_new_thread(m, (ioloop,))
        time.sleep(2)
        print u'第%s次' % count
        ioloop.stop()
        count += 1