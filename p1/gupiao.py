# coding=utf-8
'''
Created on 2015年3月30日
获取股票
@author: Administrator
'''


import xlwt

w = xlwt.Workbook()
sheet = w.add_sheet('sheet1')

for x in range(0, 60000):
    for y in range(0, 10):
        sheet.write(x, y, u'测试数据')

w.save('1.xls')
