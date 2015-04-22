# coding=utf-8
'''
Created on 2015年4月16日
中华女子学院新闻爬虫
用到的第三方包有beautifulsoup4,xlwt,html5lib(bs4所用的解析器,比默认解析器容错率好),splilnter
@author: Administrator
'''
from bs4 import BeautifulSoup as BS
import urllib
import sqlite3
import time
import xlwt
from splinter import Browser
import re


DB_FILE = '../../xinwen/sqlite.db'  # sqlite数据库文件

XINXI_URL = 'http://portal.cwu.edu.cn'
XINXI_LIST = ('xytz', 'xyxw', 'bmtz', 'bmtx', 'jwtz', 'xsgz', 'zygg')
XINXI_TEMPLATE = 'http://portal.cwu.edu.cn/%s/index%s.htm'
USERNAME = '110501059'
PASSWORD = 'mamaqaz'

# 教务通知url地址模板,2个%d分别是现在页数和每页记录数
JIAOWUTONGZHI_URL_TEMPLATE = 'http://jw.cwu.edu.cn/homepage/infoArticleList.do?sortColumn=publicationDate&columnId=10310&sortDirection=-1&pagingPage=%d&pagingNumberPer=%d'


def xinxi(is_first=False):
    browser = login()
    for each in XINXI_LIST:
        browser.visit(XINXI_TEMPLATE % (each, ''))
        soup = BS(browser.html)
        # 获取总页数
        page_div = soup.select('div#pageId')[0]
        innerhtml = page_div.find('form').get_text()
        m = re.search(ur'共\d+页', innerhtml)
        total_page = m.group()[1:len(m.group()) - 1]
        # print total_page
        lis = soup.select('ul#black')[0].find_all('li')
        handler_xinxi_lis(lis, each, is_first)  # 获取第一页的数据
        # 获取其他页的数据
        if is_first:
            for x in range(1, int(total_page)):
                browser.visit(XINXI_TEMPLATE % (each, x))
                soup = BS(browser.html)
                lis = soup.select('ul#black')[0].find_all('li')
                handler_xinxi_lis(lis, each, is_first)


def handler_xinxi_lis(lis, url, is_first):
    con = get_con()
    cur = con.cursor()

    for li in lis:
        links = 'http://portal.cwu.edu.cn/' + url + '/' + li.find_all('a')[0]['href']
        title = li.find_all('a')[0]['title']
        rel_time = li.find_all('span')[0].get_text()
        unuse_section = li.find_all('span')[1].get_text()
        m = re.search(ur'\[\*+\]', unuse_section)
        section = m.group()[1:len(m.group()) - 1]
        if is_first:
            cur.execute('insert into xinwenshow_news(title,rel_time,links,section,type) values(?,?,?,?,?)', (title, rel_time, links, section, url))
            print title, rel_time, links, section
        else:  # 取出数据来比对
            max_rel_time_rows = cur.execute("""
                select title, rel_time from xinwen where section<>? and rel_time=(
                    select max(rel_time) from xinwenshow_news)
                                            """ , (url,))
            max_rel_titles = []  # 最大时间的title列表
            for row in max_rel_time_rows:
                max_rel_titles.append(row[0])
                max_rel_time = row[1]
            if rel_time >= max_rel_time and title not in max_rel_titles:  # 对比,如果html里的时间>=最大时间且title不相同
                cur.execute('insert into xinwenshow_news(title,rel_time,links,section) values(?,?,?,?)', (title, rel_time, links, u'教务通知'))
                print title, rel_time, links, section
    con.commit()
    con.close()


def login():
    b1 = Browser() 
    b1.visit(XINXI_URL)  # 访问登陆页
    b1.fill('userName', USERNAME)  # 填写username

    b1.fill('password', PASSWORD)  # 填写password

    b1.find_by_css('input')[2].click()  # 点击登陆
    return b1


# 获取数据库连接
def get_con():
    return sqlite3.connect(DB_FILE)


# 处理教务通知html中的li列表
def handler_lis(lis, page, num_per_page, is_first=False):
    con = get_con()
    cur = con.cursor()
    insert_number = 0  # 记录插入了多少行
    for li in lis:
        title = li.find('div').find('a').get_text().replace(' ', '').replace('\n', '').replace('\r', '')  # title有很多空格和换行
        links = 'http://jw.cwu.edu.cn/homepage/' + li.find('div').find('a')['href']
        rel_time = li.find('div').find('span').get_text()
        if is_first:  # 如果是第一次扒取,不需要比对数据,直接插入
            cur.execute('insert into xinwenshow_news(title,rel_time,links,section,type) values(?,?,?,?,?)', (title, rel_time, links, u'教务处', 'jwtz'))
        else:  # 如果不是第一次扒取,需要和原有数据库里的数据比对,避免重复插入
            max_rel_time_rows = cur.execute("""
                select title, rel_time from xinwenshow_news where type='jwtz' and rel_time=(
                    select max(rel_time) from xinwenshow_news)
                                            """)
            max_rel_titles = []  # 最大时间的title列表
            for row in max_rel_time_rows:
                max_rel_titles.append(row[0])
                max_rel_time = row[1]
            if rel_time >= max_rel_time and title not in max_rel_titles:  # 对比,如果html里的时间>=最大时间且title不相同
                cur.execute('insert into xinwenshow_news(title,rel_time,links,section,type) values(?,?,?,?,?)', (title, rel_time, links, u'教务处', 'jwtz'))
                insert_number += 1
    con.commit()
    con.close()
    if insert_number == num_per_page:  # 如果这页全部数据都插入数据库就表示,第二页可能还有新的数据
        jiaowuchu(fp=None, page=page + 1, num_per_page=num_per_page)


def jiaowuchu(fp=None, page=1, num_per_page=20):
    '''
    如果传入本地文件,就是第一次扒取教务处通知,直接解析本地文件,否则,获取第一页
    '''
    if fp:
        soup = BS(open(fp), 'html5lib')  # 指定用html5lib解析器
    else:
        html = urllib.urlopen(JIAOWUTONGZHI_URL_TEMPLATE % (page, num_per_page))
        soup = BS(html, 'html5lib')  # 指定用html5lib解析器

    ul = soup.find('ul', attrs={'class': 'articleList'})
    lis = ul.find_all('li')
    if fp:
        handler_lis(lis, page, num_per_page, is_first=True)
    else:
        handler_lis(lis, page, num_per_page, is_first=False)


def excel(file_name):
    con = get_con()
    cur = con.cursor()

    w = xlwt.Workbook()
    s = w.add_sheet('sheet1')
    rows = cur.execute('select * from xinwen')
    for index, row in enumerate(rows):
        for k, v in enumerate(row):
            s.write(index, k, v)

    w.save(file_name)
    con.close()


if __name__ == '__main__':
    jiaowuchu('jiaowuchu.html')  # 首次扒取教通知,从本地文件获取数据
    # excel('1.xls')         # 将新闻从数据库取出,保存到1.xls
    jiaowuchu()  # 从网上扒取教务通知,可以添加定时任务
    xinxi(True)  # 首次扒取新闻页
    # xinxi(False)       # 添加定时任务扒取新闻页
