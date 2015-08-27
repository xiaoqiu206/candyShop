# coding=utf-8
'''
Created on 2015年8月18日

@author: Administrator
'''
import sqlite3
'''
con = sqlite3.connect('phone.db')
cur = con.cursor()
phones = ['1231123', '445524655', '445535555']

# rows = cur.executemany(
#   "insert into phone(phone,import_time) values(?,?)", [(phone, 'time') for phone in phones])
sql = 'select phone from phone;'
cur.execute(sql)
rows = cur.fetchall()
print rows
'''
print file('1.txt', 'r').readlines()
