# coding=utf-8
'''
Created on 2015年7月5日

@author: Administrator
'''
import logging
import time
from logging.handlers import TimedRotatingFileHandler


def abc():
    while 1:
        try:
            a = 5 / 0
        except Exception, e:
            logger.error(str(e), exc_info=True)
        print 123
        time.sleep(0.1)

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    handler = TimedRotatingFileHandler('hello.log', when='M', encoding='utf-8')
    handler.setLevel(logging.INFO)

    fmt = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(fmt)

    logger.addHandler(handler)

    logger.info(u'hello baby真的真的')
    abc()
