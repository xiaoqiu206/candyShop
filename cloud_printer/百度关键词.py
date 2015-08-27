# coding=utf-8
'''
Created on 2015年8月6日
百度关键词搜索任务
@author: Administrator
'''
import gevent.monkey
gevent.monkey.patch_all()
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import random
import gevent
import urllib
import Queue
import logging
import time

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='baidu.log',
    filemode='w'
)
URL = 'https://www.baidu.com/baidu?tn=monline_6_dg&ie=utf-8&wd=%s'
count = 1


def get_hanzi():
    return unichr(random.randint(0x4E00, 0x9FBF))


def get_now():
    return time.strftime('%H:%M:%S', time.localtime())


def baidu_search(q):
    hanzi = q.get()
    html = urllib.urlopen('http://www.baidu.com/baidu?' +
                          urllib.urlencode({'tn': 'monline_4_dg', 'wd': hanzi})).read()
    # print html
    # logging.info(hanzi)
    print get_now(), hanzi, len(html), q.qsize()
    baidu_search(q)


def main():
    q = Queue.Queue(0)
    for _ in range(10000):
        q.put(get_hanzi())

    threads = []
    for _ in range(10):
        threads.append(gevent.spawn(baidu_search, q))
    gevent.joinall(threads)

if __name__ == '__main__':
    main()
