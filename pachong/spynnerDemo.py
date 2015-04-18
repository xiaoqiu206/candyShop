# coding=utf-8
'''
Created on 2015年4月11日
spynner的小demo
@author: Administrator
'''
import spynner
import pyquery
import time
from bs4 import BeautifulSoup as BS


browser = spynner.Browser()
browser.show()
browser.load('http://odds.500.com/fenxi/ouzhi-452241.shtml?ctype=2')
print browser.html.encode('utf-8')
