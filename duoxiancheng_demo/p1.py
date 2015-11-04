# coding=utf-8
'''
Created on 2015年5月25日
多线程爬虫
@author: Administrator
'''
import urllib
from time import ctime
import logging
from bs4 import BeautifulSoup as BS
import threading

logger = logging.getLogger()
handler = logging.FileHandler('p1.log')
logger.addHandler(handler)
logger.setLevel(logging.NOTSET)


class MyThread(threading.Thread):

    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url

    def run(self):
        getFromUrl(self.url)


def getFromUrl(url):
    html = urllib.urlopen(url).read()
    soup = BS(html)
    logger.info(soup.title.encode('utf-8'))
    print ctime()

urls = ('http://www.baidu.com',
        'http://www.sina.com',
        'http://www.163.com',
        'http://www.ganji.com',
        'http://www.58.com',
        'http://www.youku.com',
        'http://www.tudou.com',
        'http://www.github.com',
        'http://www.stackoverflow.com',
        'http://www.sourceforge.net',
        'http://www.jd.com',
        )


def main():
    threads = []
    for url in urls:
        myThread = MyThread(url)
        threads.append(myThread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()
#     for url in urls:
#         getFromUrl(url)
    print 'end'
