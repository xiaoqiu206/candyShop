# coding=utf-8
'''
Created on 2015年3月30日
xlr的demo
@author: Administrator
'''
import xlwt


w = xlwt.Workbook()
sheet = w.add_sheet('sheet')
sheet.write(0, 0, 1)
sheet.write(0, 1, 2)
sheet.write(1, 0, '1')
sheet.write(1, 0, '2')
