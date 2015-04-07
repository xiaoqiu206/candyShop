# coding=utf-8
'''
Created on 2015年3月29日
xlwt的demo
@author: Administrator
'''
import xlwt
import tkFileDialog

w = xlwt.Workbook()
sheet = w.add_sheet('sheet1')
style = xlwt.XFStyle()
font = xlwt.Font()
font.name = 'SimSun'
style.font = font
sheet.write(1, 2, u'excel读写测试')
filename = tkFileDialog.askdirectory( initialdir="/", title='Pick a directory')
w.save(filename + '/a.xls')
