# coding=utf-8
'''
Created on 2015年4月13日
splinter的小demo
@author: Administrator
'''
import time
from splinter import Browser


browser = Browser()
browser.visit('http://www.baidu.com')
browser.execute_script("document.location.href='https://consumeprod.alipay.com/record/advanced.htm'")


print type(browser.html)
