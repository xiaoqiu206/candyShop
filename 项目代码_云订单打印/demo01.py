# coding=utf-8
'''
Created on 2015年8月6日
获取手机的user-agent
@author: Administrator
'''
import urllib
import json

url = 'http://kw.hlgimg.com/browser.php'

for _ in range(1000):
    html = urllib.urlopen(url).read()
    name = json.loads(html)['name']
    print name