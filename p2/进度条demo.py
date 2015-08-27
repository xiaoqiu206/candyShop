# coding=utf-8
'''
Created on 2015年8月1日

@author: Administrator
'''
from progressbar import ProgressBar
import time

pbar = ProgressBar(maxval=10).start()
for i in range(1, 11):
    pbar.update(i)
    time.sleep(1)
pbar.finish()
