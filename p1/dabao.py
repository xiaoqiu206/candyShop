# coding=utf-8
'''
Created on 2015年3月29日
打包程序
@author: Administrator
'''
from distutils.core import setup
import py2exe

option = {
    'py2exe':{
        'includes':['xlwt','bs4','Tkinter','urllib']
    }
}
setup( options = option,
    windows=['football.py']
)