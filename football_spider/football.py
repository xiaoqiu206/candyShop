# coding=utf-8
'''
Created on 2015年4月25日
足球比赛按照指定的指数声音提示 http://bf.310v.com/3.html
@author: Administrator
'''
from splinter import Browser
from bs4 import BeautifulSoup as BS
import time
import re
from config import DAXIAOPAN, YAPAN
import winsound


browser = Browser()
browser.visit('http://www.baidu.com')
browser.execute_script("window.location.href = 'http://bf.310v.com/3.html'")
time.sleep(10)
while True:
    soup = BS(browser.html, 'html5lib')
    table = soup.select('table#idt')[0]
    a3_trs = table.find_all('tr', class_='a3')
    a4_trs = table.find_all('tr', class_='a4')
    a3_trs.extend(a4_trs)
    for tr in a3_trs:
        if not tr.has_attr('style'):  # 没有 style='display: none'
            time_td_text = tr.find_all('td')[3].get_text()  # 比赛时间所在的td
            if re.match(r'\d+', time_td_text) and int(time_td_text) < 45:
                num1_td = tr.find_all('td')[9]
                num2_td = tr.find_all('td')[11]
                yapan1 = num1_td.find_all('div')[0].get_text()
                yapan2 = num2_td.find_all('div')[0].get_text()
                daxiaopan1 = num1_td.find_all('div')[1].get_text()
                daxiaopan2 = num2_td.find_all('div')[1].get_text()
                
                now = time.strftime('%H:%M:%S  ', time.localtime(time.time()))  # 当前时间
                tds = tr.find_all('td')
                ftype = tds[1].find('font').get_text()  # 比赛类型
                gamestarttime = tds[2].get_text()
                gamestatus = tds[3].get_text() + "'"
                team1 = tds[4].find_all('font')[2].get_text()
                score = tds[5].get_text()
                team2 = tds[6].find_all('font')[0].get_text()
                halfscore = tds[7].get_text()
                #  print gamestarttime, team1, team2, yapan1, yapan2
                for each in YAPAN:
                    # print now, ftype, gamestarttime, gamestatus, team1, score, team2, halfscore, yapan1, yapan2, u'设置好的数字:', each.split('-')[0], each.split('-')[1]
                    if yapan1 == each.split('-')[0] and yapan2 == each.split('-')[1]:
                        try:
                            winsound.PlaySound('nokia.wav', winsound.SND_PURGE)
                        except:
                            pass
                        print now, ftype, gamestarttime, gamestatus, team1, score, team2, halfscore, yapan1, yapan2, u'设置好的数字:', each.split('-')[0], each.split('-')[1]
                for each in DAXIAOPAN:
                    # print now, ftype, gamestarttime, gamestatus, team1, score, team2, halfscore, daxiaopan1, daxiaopan2, each.split('-')[0], each.split('-')[1]
                    if daxiaopan1 == each.split('-')[0] and daxiaopan2 == each.split('-')[1]:
                        try:
                            winsound.PlaySound('nokia.wav', winsound.SND_PURGE)
                        except:
                            pass
                        print now, ftype, gamestarttime, gamestatus, team1, score, team2, halfscore, daxiaopan1, daxiaopan2, u'设置好的数字:', each.split('-')[0], each.split('-')[1]
    time.sleep(10)
