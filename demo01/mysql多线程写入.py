# coding=utf-8
'''
Created on 2015年11月7日

@author: xiaoq
'''
import MySQLdb
import threading
import time
import random

_MYSQL_CON = None
_MYSQL_CUR = None


def get_mysql_con():
    '单例模式'
    global _MYSQL_CON
    if not _MYSQL_CON:
        host = '127.0.0.1'
        user = 'root'
        passwd = '123321'
        db = 'test'

        _MYSQL_CON = MySQLdb.connect(
            host=host, user=user, passwd=passwd, db=db, port=3306)
    return _MYSQL_CON


def log(uid, con):
    try:
        cur = con.cursor()
        data = (uid,)
        cur.execute("insert into demo01(name) values (%s)", data)
        con.commit()
        cur.close()
    except Exception, e:
        print time.strftime('%H:%M:%S', time.localtime()), e


class MyThread(threading.Thread):

    def __init__(self, uid, con):
        threading.Thread.__init__(self)
        self.uid = uid
        self.con = con

    def run(self):
        time.sleep(random.random())
        log(self.uid, self.con)


def main():
    ts = str(range(2))
    threads = []
    con = get_mysql_con()
    for t in ts:
        threads.append(MyThread(t, con))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    while 1:
        main()
        time.sleep(4)
