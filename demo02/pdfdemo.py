# coding=utf-8
'''
Created on 2016年1月22日

@author: xiaoq
'''
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas


fpdf = '1.pdf'
w, h = landscape(A4)
c = canvas.Canvas(fpdf, pagesize=landscape(A4))
c.drawImage('1.png', 0, 0, w, h)
c.save()
print 'ok'
