#coding=utf-8
'''
Created on 2015年5月19日
python logging模块练习
@author: Administrator
'''
import logging

LOG_FILENAME = 'log.txt'
logging.basicConfig(filename=LOG_FILENAME, level=logging.NOTSET)
logging.debug('this message shoud go to the log file')

LOG_FILENAME_2 = 'log2.txt'
logging.basicConfig(filename=LOG_FILENAME_2,level=logging.DEBUG)
logging.debug('this message shoud go to the log file')