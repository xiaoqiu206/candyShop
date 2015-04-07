# coding=utf-8
'''
Created on 2015年3月31日
第一页的数据
@author: Administrator
'''
from bs4 import BeautifulSoup as BS
import sqlite3
import urllib

con = sqlite3.connect('tonghuashun.sqlite')
cur = con.cursor()

html = urllib.urlopen('http://data.10jqka.com.cn/funds/ddzz/').read()
soup = BS(html)
trs = soup.find_all('table', attrs={'class':'m_table'})[0].find_all('tr')
for tr in trs:
    tds = tr.find_all('td')
    li = (tds[0].get_text(), tds[1].find('a').get_text(), tds[2].find('a').get_text(), tds[3].get_text(), tds[4].get_text(), tds[5].get_text(), tds[6].get_text(), tds[7].get_text(), tds[8].get_text())
    sql = "insert into tonghuashun values('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (li[0], li[1], li[2], li[3], li[4], li[5], li[6], li[7], li[8])
    cur.execute(sql)
    con.commit()




