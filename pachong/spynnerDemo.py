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
browser.load('http://bf.310v.com/3.html')
browser.wait(30)
print browser.html.encode('utf-8')
