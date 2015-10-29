# coding=utf-8
'''
Created on 2015年7月5日

@author: Administrator
'''
import logging


def abc():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info('start reading database')
    
    records = {'john': 55, 'tom': 65}
    logger.debug('records: %s', records)
    logger.info('update records ...')
    
    logger.critical('非常严重的错误')
    logger.info('finish updating records')


if __name__=='__main__':
    abc()