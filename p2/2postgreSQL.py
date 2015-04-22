# coding=utf-8
'''
Created on 2015年4月22日
将csv数据传输到postgerSQL
@author: Administrator
'''
import psycopg2


con = psycopg2.connect(database='test', user='postgres', password='123321', host='localhost', port='5432')
cur = con.cursor()

count = 0
for line in open('123.csv'):
    line_array = line.split(',')

    travel_code = line_array[0]
    adult_price = line_array[1]
    travel_date = line_array[2]
    get_time = line_array[3].replace('\n', '')

    sql = """ insert into travllist_travel(travel_code,adult_price,travel_date,get_time)values('%s','%s','%s','%s') """
    cur.execute(sql % (travel_code, adult_price, travel_date, get_time))
    count += 1
    print count

con.commit()
cur.close()
con.close()