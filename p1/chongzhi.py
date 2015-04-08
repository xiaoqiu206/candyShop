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


def sure():
    url = 'http://ls.99dk.cn/Card/BuyCard_Step2.asp'
    headers = {'Host': 'ls.99dk.cn',
               'User-Agent': ua_entry.get(),
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
               'Cookie': cookie_entry.get()
              #  'X-Requested-With': 'XMLHttpRequest',
               # 'Referer': 'http://data.10jqka.com.cn/funds/ddzz/'
               }
    data = {'GameId': account_entry.get(),
            'ReGameId': account_entry.get(),
            'chargetype': "CF»áÔ±",
            'chargetype1': "CFCLUB",
            'buynumber': num_entry,
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
    print html
    soup = BS(html)
    form = soup.find_all('form', attrs={'name': 'buycard'})[0]
    inputs = form.find_all('input', attrs={'type': 'hidden'})
    postData = {}
    for each in inputs:
        postData[each['name']] = each['value']
    postData = urllib.urlencode(postData)
    req1 = urllib2.Request(url='http://ls.99dk.cn/Card/BuyCard_Step3.asp', headers=headers)
    r2 = opener.open(req1, postData)


root = Tk()
Label(root, text=u'User-Agent').grid(row=0)

ua_entry = Entry(root)
ua_entry.grid(row=1)

Label(root, text='cookie').grid(row=2)

cookie_entry = Entry(root)
cookie_entry.grid(row=3)

Label(root, text=u'购买数量:').grid(row=4)

num_entry = Entry(root)
num_entry.grid(row=5)

Label(root, text=u'充值帐号').grid(row=6)

account_entry = Entry(root)
account_entry.grid(row=7)

Button(root, text=u'确定', command=sure).grid(row=8)

root.mainloop()
























 

