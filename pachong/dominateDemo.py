# coding=utf-8
'''
Created on 2015年4月14日
使用dominate来生成html文件的demo
@author: Administrator
'''
import dominate
from dominate.tags import *

doc = dominate.document(title='Dominate your HTML')

with doc.head:
    link(rel='stylesheet', href='style.css')
    script(type='text/javascript', src='script.js')
    
with doc:
    with div(id='header').add(ol()):
        for i in ['home', 'about', 'contact']:
            li(a(i.title(), href='/%s.html' % i))
        
    with div():
        attr(cls='body')
        p('Lerem ipsum')
        
print doc
