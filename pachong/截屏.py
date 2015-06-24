# coding=utf-8
'''
Created on 2015年4月16日
截屏的功能demo
@author: Administrator
'''
from PIL import ImageGrab

im = ImageGrab.grab(bbox=(50, 100, 300, 300))
im.save('e.jpg', 'jpeg')
