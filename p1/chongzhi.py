# coding=utf-8
'''
Created on 2015年4月8日
自动充值
@author: Administrator
'''
from Tkinter import Tk, Label, Entry, Button
import urllib
import urllib2
from bs4 import BeautifulSoup as BS
import re
import time


def sure():
    while True:
        url = 'http://www.maxshu.com/Merchant/QueryUnhandleManualOrder'
        headers = {'Host': 'www.maxshu.com',
                   'User-Agent': a_ua_entry.get(),
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                   'Cookie': a_cookie_entry.get()
                  #  'X-Requested-With': 'XMLHttpRequest',
                   # 'Referer': 'http://data.10jqka.com.cn/funds/ddzz/'
                   }
        opener = urllib2.build_opener()
        req = urllib2.Request(url=url, headers=headers)
        result = opener.open(req)
        html = result.read()
        soup = BS(html)
        tbody = soup.find_all('tbody')[1]
        trs = tbody.find_all('tr')
        for tr in trs:
            if tr.find_all('td')[1].text.contains('56366'):
                req2 = urllib2.Request(url=url + '/' + tr.find_all('td')[0], headers=headers)
                result2 = opener.open(req2)
                html2 = result2.read()
                soup2 = BS(html2)
                form = soup2.find_all('form')[0]
                # 找出帐号和数量
                uls = form.find_all('ul')
                num = uls[3].text.split(':')[1]
                account = uls[8].find('input')['value']
                brun(account, num)
                inputs = form.find_all('input')
                data = {}
                for each in inputs:
                    data[each['name']] = each['value']
                data = urllib.urlencode(data)
                req = urllib2.Request(url=url, headers=headers)
                result = opener.open(req, data)
        time.sleep(10)
        
        
def brun(account, num):
    # B站的情况
    url = 'http://ls.99dk.cn/Card/BuyCard_Step2.asp'
    headers = {'Host': 'ls.99dk.cn',
               'User-Agent': b_ua_entry.get(),
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
               'Cookie': b_cookie_entry.get()
              #  'X-Requested-With': 'XMLHttpRequest',
               # 'Referer': 'http://data.10jqka.com.cn/funds/ddzz/'
               }
    data = {'GameId': account,
            'ReGameId': account,
            'chargetype': "CF»áÔ±",
            'chargetype1': "CFCLUB",
            'buynumber': num,
            'unitLabel': "¸öÔÂ",
            'BuyCardNumber': "1",
            'SalePrice': "30.00",
            'IntegralPrice': "0.00",
            'TotalMoney': "30",
            'BankName': "account",
            'ChargeMoney': "0",
            'IsServiceChargeMoney': "0",
            'PaymentType': "0",
            'ProductId': "146"
            }
    opener = urllib2.build_opener()
    req = urllib2.Request(url=url, headers=headers)
    result = opener.open(req, urllib.urlencode(data))
    html = result.read()
    inputs = re.findall(r'''<input.+type="hidden".+>''', html)
    postData = {}
    for each in inputs:
        print each.split('"')[3], each.split('"')[5]
        postData[each.split('"')[3]] = each.split('"')[5]
    req1 = urllib2.Request(url='http://ls.99dk.cn/Card/BuyCard_Step3.asp', headers=headers)
    r2 = opener.open(req1, urllib.urlencode(postData))
    print u'充值帐号:', account
    print u'充值数量:', num


root = Tk()

a_ua_label = Label(root, text='A站UA')
a_cookie_label = Label(root, text='A站cookie')
a_ua_entry = Entry(root)
a_cookie_entry = Entry(root)

b_ua_label = Label(root, text='B站UA')
b_cookie_label = Label(root, text='B站cookie')
b_ua_entry = Entry(root)
b_cookie_entry = Entry(root)

a_ua_label.grid(row=0, column=0)
a_ua_entry.grid(row=0, column=1)
a_cookie_label.grid(row=0, column=2)
a_cookie_entry.grid(row=0, column=3)

b_ua_label.grid(row=1, column=0)
b_ua_entry.grid(row=1, column=1)
b_cookie_label.grid(row=1, column=2)
b_cookie_entry.grid(row=1, column=3)

Button(root, text='确定', command=sure).grid(row=2, column=0)

root.mainloop()
























 

