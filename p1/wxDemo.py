# coding=utf-8
'''
Created on 2015年4月10日
wxpython的demo
@author: Administrator
'''
import wx.html

class MyHtmlFrame(wx.html):
    def __init__(self, parent, title):
        html = wx.html.HtmlWindow(self)
        if "gtk2" in wx.PlatformInfo:
            html.SetStandardFonts()
            
        html.SetPage("Here is some  b formatted /b   i  u text /u  /i  "
               "loaded from a  font color=\"red\" string /font .")


app = wx.PySimpleApp()
frm = MyHtmlFrame(None, "Simple HTML")
frm.show()
app.MainLoop()