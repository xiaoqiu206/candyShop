# coding=utf-8
'''
Created on 2015年4月5日
我们要从一个网站下载数据到本地excel。API说明在这里：http://api.espeedpost.com
@author: Administrator
'''

from Tkinter import Tk, Label, Button, Entry, StringVar
import xml.etree.ElementTree as ET
import xlwt
import sqlite3
import urllib
import urllib2
import time
import tkFileDialog


def getXML(page=1):
    devid = devid_entry.get()
    appid = appid_entry.get()
    appkey = appkey_entry.get()
    date = date_entry.get()

    con = sqlite3.connect('store.db')
    cur = con.cursor()
    cur.execute('update store set devid=?,appid=?,appkey=? where id=1', (devid, appid, appkey))
    con.commit()
    con.close()

    # print 'devid: ', devid
#     print 'appid: ', appid
#     print 'appkey: ', appkey
#     print 'date: ', date

    url = 'http://api.espeedpost.com/ebay/'
    val = {'devid': devid, 'appid': appid, 'appkey': appkey, 'date': date, 'page': page }
    data = urllib.urlencode(val)
    request = urllib2.Request(url, data)
    f = urllib2.urlopen(request)
    print u'获取链接'
    html = f.read()
    return html


def getToltalPages():
    root = ET.fromstring(getXML(page=1))
    if root.find('result').text == 'error':
        print root.find('message').find('errorCode').text
        print root.find('message').find('errorMsg').text
        return None
    pagination = root.find('pagination')
    
    print 'totalpages: ', pagination.find('totalpages').text
    print 'totalrecords: ', pagination.find('totalrecords').text
    
    return int(pagination.find('totalpages').text)

def getList(page=1):
    print u'解析xml'
    reList = []
    root = ET.fromstring(getXML(page))
    # root = ET.fromstring(open('sample.xml').read())
    
    if root.find('result').text == 'error':
        print root.find('message').find('errorCode').text
        print root.find('message').find('errorMsg').text
        return None
    
    pagination = root.find('pagination')

#     print 'totalpages: ', pagination.find('totalpages').text
#     print 'pagenumber: ', pagination.find('pagenumber').text
#     print 'pagerecords: ', pagination.find('pagerecords').text
#     print 'totalrecords: ', pagination.find('totalrecords').text
    
    for ebay in root.findall('ebay'):
        for j in range(0, len(ebay.find('items'))):
            reDict = {}
            reDict['ebayid'] = ebay.find('ebayid').text
            reDict['ebaysalesrecordnumber'] = ebay.find('ebaysalesrecordnumber').text

            reDict['paidtime'] = ebay.find('paidtime').text
            reDict['currency'] = ebay.find('currency').text
            reDict['gross'] = ebay.find('gross').text
            reDict['shippingcost'] = ebay.find('shippingcost').text
            reDict['shippingservice'] = ebay.find('shippingservice').text
            reDict['note'] = ebay.find('note').text

            item = ebay.find('items')[j]
            reDict['label'] = item.get('label')
            reDict['count'] = item.get('count')
            reDict['price'] = item.get('price')
            reDict['id'] = item.get('id')
            reDict['ebaytransactionid'] = item.get('transactionid')

            buyer = ebay.find('buyer')
            reDict['id2'] = buyer.find('id').text
            reDict['fullname'] = buyer.find('fullname').text
            reDict['address1'] = buyer.find('address1').text
            reDict['address2'] = buyer.find('address2').text
            reDict['city'] = buyer.find('city').text
            reDict['state'] = buyer.find('state').text
            reDict['zip'] = buyer.find('zip').text
            reDict['country'] = buyer.find('country').text
            reDict['tel'] = buyer.find('tel').text
            reDict['email'] = buyer.find('email').text
            reDict['countryCode'] = buyer.find('countryCode').text
            if ebay_entry.get():
                if reDict['ebayid'] == ebay_entry.get():
                    reList.append(reDict)
                    continue
                else:
                    continue
            reList.append(reDict)
    
    return reList


def excel():
    fileDir = tkFileDialog.askdirectory(initialdir="/", title='Pick a directory')
    def my_cmp(x, y):
        if x['country'] > y['country']:
            return -1
        elif x['country'] < y['country']:
            return 1
        else:
            if x['id2'] > y['id2']:
                return 1
            elif x['id2'] < y['id2']:
                return -1
            else:
                return 0
    if getList() is None:
        return
    
    totalPages = getToltalPages()
    reList = []
    for x in range(1, totalPages + 1):
        reList.extend(getList(page=x))

    w = xlwt.Workbook()
    s = w.add_sheet('sheet1')

    for i in (19, 21, 24):
        s.col(i).width = 6666
    for i in (1, 2, 3, 6, 8, 9, 16, 22, 23):
        s.col(i).width = 4444

    ziduan = ('currency', 'id2', 'fullname', 'address1', 'address2', 'city',
              'state', 'zip', 'country', 'label', 'count', 'gross', 'price',
               'shippingcost', 'note', 'ebayid', 'tel', 'countryCode',
               'privateNotes', 'paidtime', 'ebaysalesrecordnumber',
               'shippingservice', 'ebaytransactionid', 'id', 'email',
               'Our_Paypal', 'ebayFee'
              )
    length1 = len(ziduan)
    for n in range(0, length1):
        s.write(0, n, ziduan[n])

    length2 = len(reList)
    for x in range(1, length2 + 1):
        for y in range(0, length1):
            if y in (18, 25, 26):
                s.write(x, y, '')
            else:
                s.write(x, y, reList[x - 1][ziduan[y]])
    filename = date_entry.get() + filename_end_entry.get() + '.xls'
    w.save(fileDir + '/' + filename)
    print u'生成excel'


root = Tk()
Label(root, text='devid', width=10).grid(row=0, column=0)
Label(root, text='appid', width=10).grid(row=0, column=2)
Label(root, text='appkey', width=10).grid(row=1, column=0)
Label(root, text='date', width=10).grid(row=1, column=2)
Label(root, text='ebayid', width=10).grid(row=3, column=0)
Label(root, text='文件名后缀', width=10).grid(row=3, column=2)

e_devid = StringVar()
e_appid = StringVar()
e_appkey = StringVar()
e_date = StringVar()

devid_entry = Entry(root, width=20, textvariable=e_devid)
appid_entry = Entry(root, width=20, textvariable=e_appid)
appkey_entry = Entry(root, width=20, textvariable=e_appkey)
date_entry = Entry(root, width=20, textvariable=e_date)
ebay_entry = Entry(root, width=20)
filename_end_entry = Entry(root, width=20)

devid_entry.grid(row=0, column=1)
appid_entry.grid(row=0, column=3)
appkey_entry.grid(row=1, column=1)
date_entry.grid(row=1, column=3)
ebay_entry.grid(row=3, column=1)
filename_end_entry.grid(row=3, column=3)

con = sqlite3.connect('store.db')
cur = con.cursor()
row = cur.execute('select * from store')
result = row.next()

nowDate = time.strftime('%Y-%m-%d', time.localtime(time.time()))

e_devid.set(result[0])
e_appid.set(result[1])
e_appkey.set(result[2])
e_date.set(nowDate)

Button(root, text='确定', command=excel, width=20).grid(row=4)
print u'生成窗口'
con.close()
root.mainloop()
