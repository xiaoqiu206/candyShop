# coding=utf-8
'''
Created on 2015年4月22日
将csv数据传输到postgerSQL,在config里设置postgresql数据库配置,第13行,配置CSV文件
@author: Administrator
'''
import psycopg2
from config import *
import time
import csv


CSV_FILE = 'Daily4UM.csv'  # csv文件的路径+文件名

MONTH2NUM = {'Jan': '01', 'Feb': '02', 'Mar': '03',
             'Apr': '04', 'May': '05', 'Jun': '06',
             'Jul': '07', 'Aug': '08', 'Sep': '09',
             'Oct': '10', 'Nov': '11', 'Dec': '12'
             }


def format_date(unformat_date):
    data_list = unformat_date.split(' ')
    day = data_list[0].zfill(2)
    month = MONTH2NUM[data_list[1]].zfill(2)
    year = data_list[2]
    return '-'.join((year, month, day))


def upload():
    con = psycopg2.connect(database=PGSQL_DBNAME, user=PGSQL_USERNAME, password=PGSQL_PASSWORD, host=PGSQL_HOST, port=PGSQL_PORT)
    cur = con.cursor()
    reader = csv.reader(file(CSV_FILE, 'rb'))
    for code, adultprice, date, signdate in reader:
        if date.find('date') == -1:
            update_or_save(code, adultprice, date, signdate, con, cur)


def update_or_save(travel_code, adults_price, travel_date, get_time, pg_con, pg_cur):
    travel_date = format_date(travel_date)
    select_sql = "select count(*) from travllist_travel where travel_code=%s and travel_date=%s"
    pg_cur.execute(select_sql, (travel_code, travel_date))
    rows = pg_cur.fetchall()
    if rows[0][0] == 0:
        insert_template = "insert into travllist_travel(travel_code, travel_date,adult_price,get_time)values(%s,%s,%s,%s)"
        pg_cur.execute(insert_template, (travel_code, travel_date, adults_price, get_time))
        print time.strftime('%H:%M:%S', time.localtime(time.time())), u'增加数据', travel_code, travel_date, adults_price
    else:
        update_template = "update travllist_travel set adult_price=%s,get_time=%s where travel_code=%s and travel_date=%s"
        pg_cur.execute(update_template, (adults_price, get_time, travel_code, travel_date))
        print time.strftime('%H:%M:%S', time.localtime(time.time())), u'更新数据', travel_code, travel_date, adults_price
    pg_con.commit()


if __name__ == '__main__':
    upload()
