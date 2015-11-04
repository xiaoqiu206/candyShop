# coding=utf-8
'''
Created on 2015年3月31日
同花顺大交易数据采集
@author: Administrator
'''
import urllib2
import urllib
import sqlite3
import json
from bs4 import BeautifulSoup as BS
import xlwt
from Tkinter import Button, Label, Tk, Entry, StringVar
import time


def firstPage():
    con = sqlite3.connect('tonghuashun.sqlite')
    cur = con.cursor()

    html = urllib.urlopen('http://data.10jqka.com.cn/funds/ddzz/').read()
    soup = BS(html)
    trs = soup.find_all('table', attrs={'class':'m_table'})[0].find_all('tr')
    for tr in trs[1:]:
        tds = tr.find_all('td')
        li = (tds[0].get_text(), tds[1].find('a').get_text(), tds[2].find('a').get_text(), tds[3].get_text(), tds[4].get_text(), tds[5].get_text(), tds[6].get_text(), tds[7].get_text(), tds[8].get_text())
        sql = "insert into tonghuashun values('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (li[0], li[1], li[2], li[3], li[4], li[5], li[6], li[7], li[8])
        cur.execute(sql)
        con.commit()
        label['text'] = u'第一页导入成功'
    con.close()


def otherPage():
    con = sqlite3.connect('tonghuashun.sqlite')
    cur = con.cursor()
    headers = {'Host': 'data.10jqka.com.cn',
               'User-Agent': ua_entry['text'],
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
               'Cookie': cookie_entry['text'],
               'X-Requested-With': 'XMLHttpRequest',
               'Referer': 'http://data.10jqka.com.cn/funds/ddzz/'
               }
    opener = urllib2.build_opener()
    for page in range(int(e.get()), int(e1.get()) + 1):
        label['text'] = u'正在导入第%d页' % page, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        url = 'http://data.10jqka.com.cn/interface/funds/ddzz/zdf/desc/' + str(page) + '/null/'
        req = urllib2.Request(url=url, headers=headers)
        try:
            result = opener.open(req)
        except:
            print  u'服务器出错,10秒后再次连接'
            time.sleep(10)
            result = opener.open(req)
        jsonData = json.loads(result.read())
        soup = BS(jsonData['data'])
        trs = soup.find_all('tr')
        for tr in trs:
            tds = tr.find_all('td')
            li = (tds[0].get_text(), tds[1].find('a').get_text(), tds[2].find('a').get_text(), tds[3].get_text(), tds[4].get_text(), tds[5].get_text(), tds[6].get_text(), tds[7].get_text(), tds[8].get_text())
            sql = "insert into tonghuashun values('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (li[0], li[1], li[2], li[3], li[4], li[5], li[6], li[7], li[8])
            cur.execute(sql)
            con.commit()
        print u'导入第%d页成功' % page, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
   
    con.close()


def deleteData():
    con = sqlite3.connect('tonghuashun.sqlite')
    cur = con.cursor()
    cur.execute('delete from tonghuashun')
    con.commit()
    con.close()
    label['text'] = u'清空数据库成功'


def excel():
    con = sqlite3.connect('tonghuashun.sqlite')
    cur = con.cursor()
    rows = cur.execute('select * from tonghuashun')
    w = xlwt.Workbook()
    s = w.add_sheet('sheet1')
    x = 0
    for row in rows:
        y = 0
        for one in row:
            s.write(x, y, one)
            y += 1
        x += 1
    con.close()
    file_name = time.strftime('%Y-%m-%d %H,%M,%S', time.localtime(time.time())) + '.xls'
    w.save(file_name)
    label['text'] = file_name

root = Tk()
Button(root, text='清空数据库', command=deleteData, width=20).grid(row=0, column=0)
Button(root, text='导入第一页', command=firstPage, width=20).grid(row=0, column=1)
Button(root, text='导入其他指定页', command=otherPage, width=20).grid(row=0, column=2)
Button(root, text='导出到excel', command=excel, width=20).grid(row=0, column=3)
label = Label(root, text='', width=20)

ua_label = Label(root, text='请输入user-agent')
cookie_label = Label(root, text='请输入cookie')
page_label = Label(root, text='请输入开始页数(大于1)')
maxpage_label = Label(root, text='请输入结束页数')

ua_entry = Entry(root)
cookie_entry = Entry(root)

e = StringVar()
page_entry = Entry(root, textvariable=e)
e.set('2')

e1 = StringVar()
maxpage_entry = Entry(root, textvariable=e1)
e1.set('3')

ua_label.grid(row=1, column=0)
cookie_label.grid(row=1, column=2)
ua_entry.grid(row=1, column=1)
cookie_entry.grid(row=1, column=3)


page_label.grid(row=2, column=0)
page_entry.grid(row=2, column=1)
maxpage_entry.grid(row=2, column=3)
maxpage_label.grid(row=2, column=2)

label.grid(row=3, column=0)


root.mainloop()
