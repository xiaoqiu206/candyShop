# coding=utf-8
'''
Created on 2015年6月26日
tornado httpclient post request
@author: Administrator
'''
from gevent import monkey
monkey.patch_all()
import gevent
import urllib
import time

count = 0


def f(url):
    global count
    count += 1
    if count == 3:
        f('http://www.aliyun.com')
    data = urllib.urlopen(url).read()
    print url, len(data)



def main():
    gevent.joinall(
        [
            gevent.spawn(f, 'http://www.sina.com'),
            gevent.spawn(f, 'http://www.baidu.com'),
            gevent.spawn(f, 'http://www.163.com'),
            gevent.spawn(f, 'http://www.qq.com'),
            gevent.spawn(f, 'http://www.51cto.com'),
            gevent.spawn(f, 'http://www.csdn.net')
        ]
    )

if __name__ == '__main__':
    t1 = time.time()
    main()
    # main2()
    print time.time() - t1
