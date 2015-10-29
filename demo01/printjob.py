#coding=utf-8
'''
Created on 2015年5月22日

@author: Administrator
'''
import time

while 1:
    import config
    reload(config)
    print config.ABC
    time.sleep(3)