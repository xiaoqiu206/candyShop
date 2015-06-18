#coding=utf-8
'''
Created on 2015年5月19日
不同的日志写入不同的文件
@author: Administrator
'''
import logging


def setLog(log_filename, log_message):
    logger = logging.getLogger()
    handler = logging.FileHandler(log_filename)
    logger.addHandler(handler)
    logger.setLevel(logging.NOTSET)
    logger.debug(log_message)
    
    # logger.removeHandler(handler)
    

if __name__ == '__main__':
    setLog('log_test', 'it is all right')
    setLog('log_test88', 'it is all right55')
    setLog('log_test66', 'it is all right999')