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


from gevent.queue import Queue


def insert_data(data):
    gevent.sleep(0.5)
    q.put(data)


def insert():
    con = pymysql.connect(
        host='127.0.0.1', user='root', passwd='123321', db='test', port=3306)
    cur = con.cursor()
    gevent.sleep(0.6)
    while 1:
        try:
            data = q.get(False)
        except Exception:
            break
        else:
            cur.execute("insert into demo02 values(%s)" % data)
            print '已插入', data
    con.commit()
    cur.close()
    con.close()

if __name__ == "__main__":
    q = Queue(100)
    while 1:
        data_list = range(5)
        gs = [gevent.spawn(insert_data, str(data))
              for data in data_list]
        gs.append(gevent.spawn(insert))
        gevent.joinall(gs)
        time.sleep(1)
        print '休眠3秒'
