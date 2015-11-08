# coding=utf-8
'''
Created on 2015年11月7日

@author: xiaoq
'''
from gevent import monkey
monkey.patch_all()
import urllib
import gevent


def get_html(*args):
    print args
    url = args[0]
    flag = args[1]
    print len(urllib.urlopen(url).read())
    if url.find('qq') > -1:
        get_html('http://www.51cto.com')
        get_html('http://www.aliyun.com')
        get_html('http://www.csdn.net')


if __name__ == '__main__':
    urls = (
        'http://www.qq.com',
        'http://www.github.com'
    )

    g1 = gevent.spawn(get_html, (urls[0], 1))
    g2 = gevent.spawn(get_html, (urls[1], 0))
    g3 = gevent.spawn()
    gevent.joinall((g1, g2))
