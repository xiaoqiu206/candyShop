# coding=utf-8
'''
Created on 2015年11月12日
mysqldb和pymysql速度对比
@author: xiaoq
'''
import MySQLdb
import pymysql

host = '121.40.176.181'
user = 'cmtaotangmicom'
passwd = '231f5407'
db = 'cmtaotangmicom'


def db1_insert():
    con = MySQLdb.connect(
        host=host, user=user, passwd=passwd, db=db, port=3306)
    cur = con.cursor()
    cur.execute(
        "insert into push_log(event,local_data) values('test', 'test')")
    con.commit()
    cur.close()
    con.close()


con = pymysql.connect(
    host=host, user=user, passwd=passwd, db=db, port=3306)
cur = con.cursor()


def db2_insert():
    cur.execute(
        "insert into push_log(event,local_data) values('test', 'test')")


import time


t2 = time.time()
for _ in range(50):
    db2_insert()
con.commit()
cur.close()
con.close()
t3 = time.time()

print t3 - t2
