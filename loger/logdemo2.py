#coding=utf-8
'''
Created on 2015年5月19日

@author: Administrator
'''
import logging

logger = logging.getLogger()
handler = logging.FileHandler('logdemo2.txt')
logger.addHandler(handler)
logger.setLevel(logging.NOTSET)
logger.error('this is an error message')
logger.info('this is an info message')
logger.critical('this is a critical message')