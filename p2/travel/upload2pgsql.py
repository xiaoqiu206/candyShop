# coding=utf-8
'''
Created on 2015年4月24日
上传到postgreSQL数据库
@author: Administrator
'''
import psycopg2
from config import *
import sqlite3
import time

MONTH = {'Jan': '01', 'Feb': '02', 'Mar': '03',
             'Apr': '04', 'May': '05', 'Jun': '06',
             'Jul': '07', 'Aug': '08', 'Sep': '09',
             'Oct': '10', 'Nov': '11', 'Dec': '12'
             }

def upload2pgsql():
    pg_con = psycopg2.connect(database=PGSQL_DBNAME, user=PGSQL_USERNAME, password=PGSQL_PASSWORD, host=PGSQL_HOST, port=PGSQL_PORT)
    pg_cur = pg_con.cursor()

    st_con = sqlite3.connect('travel.db')
    st_cur = st_con.cursor()

    rows = st_cur.execute(SELECT_SQL)
    for row in rows:
        update_or_save(row, pg_con, pg_cur)
    pg_con.close()
    st_con.close()


def update_or_save(row, pg_con, pg_cur):
    travel_code = row[1]
    travel_date = row[2]
    if travel_date.find(' ') != -1:  # 如果日期里包含空格
        datelist = travel_date.split(' ')
        travel_date = datelist[2] + '-' + MONTH[datelist[1]] + '-' + datelist[0].zfill(2)
    adults_price = row[3]
    children_price = row[4]
    remark = row[5]
    get_time = row[6]

    select_sql = "select count(*) from travllist_travel where travel_code=%s and travel_date=%s"
    pg_cur.execute(select_sql, (travel_code, travel_date))
    rows = pg_cur.fetchall()
    if rows[0][0] == 0:
        insert_template = "insert into travllist_travel(travel_code, travel_date,adult_price,child_price,remark,get_time)values(%s,%s,%s,%s,%s,%s)"
        pg_cur.execute(insert_template, (travel_code, travel_date, adults_price, children_price, remark if UPLOAD_REMARK else '', get_time))
        print time.strftime('%H:%M:%S', time.localtime(time.time())), u'增加数据', travel_code, travel_date, adults_price, children_price
    else:
        update_template = "update travllist_travel set adult_price=%s, child_price=%s ,remark=%s, get_time=%s where travel_code=%s and travel_date=%s"
        pg_cur.execute(update_template, (adults_price, children_price, remark if UPLOAD_REMARK else '' , get_time, travel_code, travel_date))
        print time.strftime('%H:%M:%S', time.localtime(time.time())), u'更新数据', travel_code, travel_date, adults_price, children_price
    pg_con.commit()


if __name__ == '__main__':
    upload2pgsql()
    print u'上传完成,100秒后窗口自动关闭'
    time.sleep(100)
