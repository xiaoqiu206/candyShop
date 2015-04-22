# coding=utf-8
'''
Created on 2015年4月20日
抓取足彩数据,并提醒
@author: Administrator
'''
from splinter import Browser
from bs4 import BeautifulSoup as BS
import time
import winsound


b1 = Browser()
b1.visit('http://bf.310v.com/3.html')
ignore_list = []
while 1:
    soup = BS(b1.html, 'html5lib')
    table = soup.find(id='idt')
    tbody = table.find_all('tbody')[0]
    tr3s = tbody.find_all('tr', attrs={'class': 'a3'})
    tr4s = tbody.find_all('tr', attrs={'class': 'a4'})
    trs = tr3s + tr4s
    for tr in trs:
        if not tr.get('id').startswith('ad'):
            tds = tr.find_all('td')
            name = tds[1].get_text()  # 联赛名称
            ftime = tds[2].get_text()  # 时间
            status = tds[3].get_text()  # 状态
            team1 = tds[4].find_all('font')[2].get_text()  # 主场球队
            score = tds[5].get_text()  # 比分
            team2 = tds[6].find_all('font')[0].get_text()  # 客场球队
            banchang = tds[7].get_text()  # 半场
            num1 = tds[9].find_all('div')[0].get_text()  # 指数
            sb = tds[10].find_all('div')[0].get_text()  # SB 我也不知道是什么
            num2 = tds[11].find_all('div')[0].get_text()  # 指数
            # print name, ftime, status, team1, score, team2, banchang, num1, sb, num2
            for line in open('config'):
                nums = line.split('-')
                if nums[0] == num1 and nums[len(nums) - 1].replace('\n', '') == num2:
                    teams = team1 + ' vs ' + team2
                    if teams not in ignore_list:
                        print name, ftime, status, team1, score, team2, banchang, num1, sb, num2
                        winsound.PlaySound('nokia.wav', 10)
                        input_word = raw_input(u'忽略' + teams + '? y/n')
                        if input_word.lower() == 'Y':
                            ignore_list.append(teams)
    time.sleep(10)

