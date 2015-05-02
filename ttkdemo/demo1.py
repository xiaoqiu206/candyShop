# coding=utf-8
'''
Created on 2015年4月30日
ttk的demo
@author: Administrator
'''
import Tkinter
import ttk
from django.utils.termcolors import background


root = Tkinter.Tk()
style = ttk.Style()
style.configure("BW.TLabel", foreground='black', background='white')

l1 = ttk.Label(root, text='Test',)
l2 = ttk.Label(root, text="Test", )

l1.pack()
l2.pack()

root.mainloop()
