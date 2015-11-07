# coding=utf-8
'''
Created on 2015年11月6日

@author: xiaoq
'''
import config
import time


r = config.get_redis_con()

while 1:
    length1 = len(filter(lambda x: x.find('user') > -1, r.keys()))
    length2 = len(r.smembers('users'))
    if length1 != 56 or length2 != 55:
        print r.keys(), config.TimeUtils.get_timestamp()
    time.sleep(2)