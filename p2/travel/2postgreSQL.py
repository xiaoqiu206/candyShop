# coding=utf-8
'''
Created on 2015年4月22日
将csv数据传输到postgerSQL
@author: Administrator
'''
import psycopg2

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


con = psycopg2.connect(database='test', user='postgres', password='123321', host='localhost', port='5432')
cur = con.cursor()

count = 0
for line in open('123.csv'):
    line_array = line.split(',')

    travel_code = line_array[0]
    adult_price = line_array[1]
    travel_date = format_date(line_array[2])
    get_time = line_array[3].replace('\n', '')

    sql = """ insert into travllist_travel(travel_code,adult_price,travel_date,get_time)values('%s','%s','%s','%s') """
    cur.execute(sql % (travel_code, adult_price, travel_date, get_time))
    count += 1
    print count

con.commit()
cur.close()
con.close()