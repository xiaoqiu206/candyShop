# coding=utf-8
'''
Created on 2015年4月30日
tk的demo,菜单项
@author: Administrator
'''
from Tkinter import *
import time


root = Tk()


def hello():
    print 'hello menu'

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
for item in [1, 2, 3, 414, 14, 1, 4]:
    filemenu.add_command(label=unicode(item), command=hello)

root['menu'] = menubar
menubar.add_cascade(label='Language', menu=filemenu)
root.mainloop()
