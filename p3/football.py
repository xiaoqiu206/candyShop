# coding=utf-8
'''
Created on 2015年4月25日
足球比赛按照指定的指数声音提示
@author: Administrator
'''
from splinter import Browser
from bs4 import BeautifulSoup as BS
import time


browser = Browser()
browser.visit('http://bf.310v.com/3.html')
time.sleep(3)
while True:
    soup = BS(browser.html, 'html5lib')
    table = soup.find_all('table', attrs={'id': 'idt'})[0]
    a3_trs = table.find_all('tr', class_='a3')
    a4_trs = table.find_all('tr', class_='a4')
    trs = a3_trs.extend(a4_trs)
    for tr in trs:
        if not tr.has_attr('style'):  # 没有 style='display: none'
            time_td = tr.find_all('td')[3]  # 比赛时间所在的td
            if time_td.get_text():  # td里有内容
                print time_td.get_text()
    time.sleep(53)
