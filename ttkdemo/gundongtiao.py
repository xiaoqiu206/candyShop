# coding=utf-8
'''
Created on 2015年5月3日
滚动条demo
@author: Administrator
'''
from Tkinter import *

root = Tk()
lb = Listbox(root)
s1 = Scrollbar(root)
s1.pack(side=RIGHT, fill=Y)

lb['yscrollcommand'] = s1.set
for i in range(100):
    lb.insert(END, str(i))
lb.see(50)
lb.pack(side=LEFT)
s1['command'] = lb.yview
root.mainloop()
