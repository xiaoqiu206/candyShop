# coding=utf-8
'''
Created on 2015年4月15日
关于python在win7网上邻居传文件
@author: Administrator
'''
import os
import time
import shutil


os.system('net use z: \\192.168.1.168\Jobs')
shutil.copy('123123123.txt', 'z:')
# print os.path.exists(r"\\192.168.1.168\Jobs")
# print os.path.exists(r"C:/CODE")
time.sleep(1000)
