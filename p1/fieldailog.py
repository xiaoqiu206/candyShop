# coding=utf-8
'''
Created on 2015年4月7日
Tkinter的文件选择对话框
@author: Administrator
'''
import Tkinter, tkFileDialog
from Tkinter import *

root = Tkinter.Tk()



def pick(): 
    dirname = tkFileDialog.askdirectory(parent=root, initialdir="/", title='Pick a directory')
    print dirname
    
Button(root, text='选择',command=pick).pack()

root.mainloop()