#coding=utf-8
'''
Created on 2015年5月27日
单例模式联系
@author: Administrator
'''
from cloud_printer import config

mem_con1 = config.get_memcache_con()
mem_con2 = config.get_memcache_con()

print mem_con1, mem_con2
print mem_con1 is mem_con2
