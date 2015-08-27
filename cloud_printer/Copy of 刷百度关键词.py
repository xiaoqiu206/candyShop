# coding=utf-8
'''
Created on 2015年8月6日

@author: Administrator
'''
from bs4 import BeautifulSoup
import requests
import gevent

import json
import sys
import time
import Queue
import urllib

import gevent.monkey
gevent.monkey.patch_all()

reload(sys)
sys.setdefaultencoding('utf-8')

BROWSER_UA_API = 'http://kw.hlgimg.com/browser.php'
# PROXY_ORDERID = 943883962837390
BAIDU_URL = 'http://m.baidu.com'
count = 0


PROXY_API = ('http://www.kuaidaili.com/api/getproxy/?orderid=923899279084284&'
             'num=1&area=%E4%B8%AD%E5%9B%BD&browser=2&protocol=1&method=1&an_tr=1'
             '&sp1=1&sp2=1&quality=1&sort=0')


PROXY_Q = Queue.Queue(100)
UA_Q = Queue.Queue(100)


def get_ua():
    '通过接口获取随机的浏览器UA'
    response = urllib.urlopen(BROWSER_UA_API)
    html = response.read()
    name = json.loads(html)['name']
    # print now(), 'get ua'
    return name


def ua_greenlet():
    if UA_Q.qsize() < 10:
        UA_Q.put(get_ua())
    gevent.sleep(0.1)
    ua_greenlet()


def proxy_greenlet():
    if PROXY_Q.qsize() < 10:
        PROXY_Q.put(get_proxy())
    gevent.sleep(0.1)
    proxy_greenlet()


def get_proxy():
    '通过接口获取代理IP'
    # locals()['orderid'] = PROXY_ORDERID
    # print PROXY_API % urllib.urlencode(locals())
    response = urllib.urlopen(PROXY_API)
    html = response.read()
    # print now(), 'get_proxy', html
    return html


def now():
    return time.strftime('%H:%M:%S', time.localtime())


def handler():
    global count
    print now(), count, 'start'
    # 获得代理
    proxy = PROXY_Q.get()
    proxies = {'http': proxy}

    # 获取浏览器user-agent
    ua = UA_Q.get()

    # 共用的会话对象
    s = requests.session()
    s.headers.update({'User-Agent': ua})
    s.headers.update({'Host': 'm.baidu.com'})

    # 访问百度移动版首页
    res1 = s.get(BAIDU_URL, proxies=proxies)
    page1 = res1.text

    # 解析百度首页,获取所有input框中的键值对
    data = {'word': '昆明外阴白斑'}
    soup = BeautifulSoup(page1, 'html5lib')

    inputs = soup.select('#index-form input')
    for each in inputs:
        data[each['name']] = each['value']
    # print data

    # 搜索关键词
    res2 = s.get(
        BAIDU_URL + '/s', params=data, proxies=proxies)
    # print res2.url

    page2 = res2.text

    '''
    # 解析主词搜索后的结果页,点击一个非推广链接
    soup2 = BeautifulSoup(page2, 'html5lib')
    try:

        href1 = (soup2.find('div', class_='result') or soup2.find(
            'div', class_='resitem')).find('a')['href']
    except Exception, e:
        print u'网页错误', page2
        return
    '''
    # 点击副链接
    data['word'] = '昆明外阴白斑军都权威'
    res4 = s.get(
        BAIDU_URL + '/s', params=data, proxies=proxies)
    page4 = res4.text
    '''
    # 解析副词搜索后的结果页,点击一个非推广链接
    soup3 = BeautifulSoup(page4, 'html5lib')
    try:
        href2 = (soup3.find('div', class_='result') or soup3.find(
            'div', class_='resitem')).find('a')['href']
    except Exception, e:
        print u'网页错误', page4
        return
    # print href
    s.get(BAIDU_URL + href1, proxies=proxies)
    s.get(BAIDU_URL + href2, proxies=proxies)
    '''
    print now(), count

    count += 1


def main_greenlet():
    try:
        handler()
    except Exception, e:
        print now(), 'ERROR', e
    main_greenlet()


def main():
    for _ in range(10):
        PROXY_Q.put(get_proxy())
        UA_Q.put(get_ua())

    threads = [gevent.spawn(ua_greenlet), gevent.spawn(proxy_greenlet)]
    for _ in range(10):
        threads.append(gevent.spawn(main_greenlet))

    gevent.joinall(threads)

if __name__ == '__main__':
    main()
    # get_proxy()
