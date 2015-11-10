# coding=utf-8
'''
Created on 2015年11月10日

@author: xiaoq
'''
from gevent import monkey
monkey.patch_all()
import gevent
import pymysql
import time


def print_time(fuc):
    def _fuc(*args):
        t1 = time.time()
        ret = fuc(*args)
        t2 = time.time()
        print args[0], '号消耗时间', t2 - t1
        return ret
    return _fuc


@print_time
def dbtest(x, con):

    cur = con.cursor()
    cur.execute('select 100 from demo01 limit 1;')
    rows = cur.fetchall()
    cur.close()
    print rows
    return rows


def empty_fn():
    pass

t1 = time.time()
con = pymysql.connect(
    host='127.0.0.1', user='root', passwd='123321', db='test', port=3306)
gevent.joinall([gevent.spawn(dbtest, x, con) for x in range(200)])
# dbtest(3, con)
t2 = time.time()
print t2 - t1
