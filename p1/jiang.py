# coding=utf-8
'''
Created on 2015年4月7日
指定中奖号码生成随机数
@author: Administrator
'''

from Tkinter import Tk, Frame, Label, Entry, Button
import sqlite3


def sure_in():
    pass


def sure_out():
    pass


root = Tk()

frame1 = Frame(root)
frame2 = Frame(root)
frame3 = Frame(root)
frame1.pack()
frame2.pack()
frame3.pack()

Label(frame1, text=u'第', width=5).grid(row=0, column=0)
qi_entry = Entry(frame1, width=5)
qi_entry.grid(row=0, column=1)
Label(frame1, text=u'期开奖号:', width=10).grid(row=0, column=2)
num_entry = Entry(frame1, width=5)
num_entry.grid(row=0, column=3)
Button(frame1, text='确定', command=sure_in).grid(row=0, column=4)

Label(frame2, text=u'选择').grid(row=0, column=0)
choice_entry = Entry(frame2, width=5)
choice_entry.grid(row=0, column=1)
Label(frame2, text=u'期').grid(row=0, column=2)
Button(frame2, text=u'生成开奖号(刷新)', command=sure_out).grid(row=0, column=3)




root.mainloop()
