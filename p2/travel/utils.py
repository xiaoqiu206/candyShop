# coding=utf-8
'''
Created on 2015年4月24日

@author: Administrator
'''
from bs4 import BeautifulSoup as BS
from splinter import Browser
import time
from config import DEADLINE_DAY, SLEEP_TIME, URL_LIST
import datetime
import sqlite3


def getdaylist():
    today = datetime.date.today()
    day_list = []
    for x in range(1, DEADLINE_DAY + 1):
        day_plus = today + datetime.timedelta(days=x)
        # format_day = '%s/%s/%s' % (str(day_plus.month).zfill(2), str(day_plus.day).zfill(2), day_plus.year)
        day_list.append(day_plus)
    return day_list


def handler_html(html):
    soup = BS(html)
    codediv = soup.find_all('div', class_='product-retail-price')[0]  # 产品代码所在div
    codep = codediv.find_all('p')[1]  # 产品代码所在p
    travel_code = codep.get_text().split(u'：')[1]  # "产品代码：BLW-4HK" 格式进行处理
    odiv = soup.find_all('div', class_='nexus_itinerary_entry_rate')[0]
    trs = odiv.find_all('tr')
    tds1 = trs[1].find_all('td')
    if tds1[0].get_text() == u'成人':
        adults_price = tds1[3].get_text()
    tds2 = trs[2].find_all('td')
    childred_price = ''
    if tds2[0].get_text() == u'儿童':
        childred_price = tds2[3].get_text()
    return (travel_code, adults_price, childred_price)


def getdata():
    con = sqlite3.connect('travel.db')
    cur = con.cursor()
    b1 = Browser()
    day_list = getdaylist()
    for url in URL_LIST:
        b1.visit(url)
        for each_day in day_list:
            b1.fill('adults', '1')  # 选择成人数量1
            b1.fill('children', '1')  # 选择儿童数量1
            format_date1 = str(each_day)  # 这种格式 YYYY-MM-DD
            format_date2 = '%s/%s/%s' % (str(each_day.month).zfill(2), str(each_day.day).zfill(2), str(each_day.year))
            date_js = "document.getElementById('itinTravelDate').value='%s';" % format_date2
            b1.execute_script(date_js)
            b1.execute_script("document.getElementById('itinGo').click();")
            time.sleep(SLEEP_TIME)
            if b1.is_element_present_by_css('.nexus_itinerary_entry_rate'):
                travel_code, adults_price, children_price = handler_html(b1.html)
                update_or_save(travel_code, format_date1, adults_price, children_price, cur, con)
    b1.quit()


def update_or_save(travel_code, travel_date, adults_price, children_price, cur, con):
    update_template = "update travel set adults_price=? and children_price=? where travel_code=? and travel_date=?"
    insert_template = "insert into travel(travel_code,travel_date,adults_price,children_price)values(?,?,?,?)"
    select_template = "select count(*) from travel where travel_code=? and travel_date=?"
    rows = cur.execute(select_template, (travel_code, travel_date))
    if rows.next()[0] == 0:
        cur.execute(insert_template, (travel_code, travel_date, adults_price, children_price))
        print time.strftime('%H:%M:%S', time.localtime(time.time())), u'增加数据', travel_code, travel_date, adults_price, children_price
    else:
        cur.execute(update_template, (travel_code, travel_date, adults_price, children_price))
        print time.strftime('%H:%M:%S', time.localtime(time.time())), u'更新数据', travel_code, travel_date, adults_price, children_price
    con.commit()
