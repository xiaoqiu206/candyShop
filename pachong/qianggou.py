# coding=utf-8
'''
Created on 2015年7月16日
日本阿卡佳抢购
@author: Administrator
'''
import threading
import xlrd
import time
from poplib import POP3
import re
from splinter import Browser
from bs4 import BeautifulSoup


class BuyThread(threading.Thread):

    def __init__(self, datalist):
        threading.Thread.__init__(self)
        self.datalist = datalist

    def run(self):
        fid, step, url, email, _card_no, _password, _sei, _mei, _sei_kana, _mei_kana,\
            _tel, email_password, popaddress, _buy_time = self.datalist
        print now(), fid, u'打开网页'
        b = Browser('phantomjs')
        b.visit('http://www.baidu.com')
        b.execute_script("document.location.href='%s'" % url)
        time.sleep(3)
        if step in ('1', u'1'):
            while 1:
                time.sleep(0.3)
                soup = BeautifulSoup(b.html, 'html5lib')
                if soup.find_all('input', attrs={'name': 'sbmt'}):
                    break
                b.reload()
                print now(), fid, u'刷新网页'
            buy(self.datalist, b)

        if step in ('2', u'2'):
            email_num1 = get_email_num(email, email_password, popaddress)
            while 1:
                time.sleep(0.3)
                soup = BeautifulSoup(b.html, 'html5lib')
                print now(), fid, u'网页字符数:', len(b.html)
                if soup.find_all('input', class_='inputTxt1').__len__() == 2:
                    break
                b.reload()
                print now(), fid, u'刷新网页'
            step2(self.datalist, b, email_num1)


def now():
    return time.strftime('%Y-%m-%d %H:%M:%S')


def get_email_num(user, passwd, popaddress):
    '获取邮箱内的邮件数量'
    try:
        p = POP3(popaddress)
        p.user(user)
        p.pass_(passwd)
        email_num = p.stat()[0]
        p.quit()
    except Exception, e:
        print now(),  u'获取邮件错误', str(e), user, passwd, popaddress
        return None
    else:
        return email_num


def get_last_email_url(user, passwd, popaddress, num):
    '获取最近一封邮件内的http链接'
    p = POP3(popaddress)
    p.user(user)
    p.pass_(passwd)
    _rsp, msg, _siz = p.retr(num)
    url = None
    for eachline in msg:
        if re.match(r'https://\S+', eachline):
            url = eachline
    return url


def check_error(browser, checkemail=None):
    if browser.is_element_present_by_css('.error'):
        return browser.find_by_css('.error').first.value

    if checkemail and browser.html.find(checkemail) == -1:
        return checkemail

    return None


def buy(datalist, b):
    fid, _step, _url, email, _card_no, _password, _sei, _mei, _sei_kana, _mei_kana,\
        _tel, email_password, popaddress, _buy_time = datalist
    print now(), fid, u'获取邮件数量...'
    print now(), fid, u'开始抢购...'
    email_num1 = get_email_num(email, email_password, popaddress)
    if not email_num1:
        return

    print now(), fid, u'点击预约'
    b.find_by_name('sbmt').first.click()

    haserror = check_error(b)
    if haserror:
        print now(), fid, u'网页错误...', haserror
        return

    if len(b.html) < 50:
        print now(), fid, u'服务器繁忙...'
        return

    step2(datalist, b, email_num1)


def step2(datalist, b, email_num1):
    fid, _step, _url, email, card_no, password, sei, mei, sei_kana, mei_kana,\
        tel, email_password, popaddress, _buy_time = datalist
    print now(), fid, u'开始填写email'
    b.find_by_name('mail1').first.fill(email)
    b.find_by_name('mail2').first.fill(email)
    b.find_by_name('sbmt').first.click()

    haserror = check_error(b)
    if haserror:
        print now(), fid, u'网页错误...', haserror
        return

    print now(), fid, u'确认邮箱...'
    b.find_by_name('sbmt').first.click()

    while 1:
        haserror = check_error(b, checkemail=email)
        if haserror:
            if haserror == email:
                print now(), fid, u'未知错误,发送邮件失败,刷新网页...', b.html
                b.reload()
                continue
            else:
                print now(), fid, u'网页错误...', haserror
                return
        else:
            break

    while 1:
        print now(), fid, u'检查邮箱内的新邮件....'
        email_num2 = get_email_num(email, email_password, popaddress)
        print now(), fid, u'原邮件数量:', email_num1, u'   现在邮件数量:', email_num2
        if email_num2 > email_num1:
            print now(), fid, u'有新邮件...'
            email_url = get_last_email_url(
                email, email_password, popaddress, email_num2)
            b.execute_script("document.location.href='%s'" % email_url)

            # 等待网页加载完成
            while 1:
                print now(), fid, u'等待网页加载'
                if b.is_element_present_by_css('.error') or b.is_element_present_by_name('card_no'):
                    break
                time.sleep(0.3)

            haserror = check_error(b)
            if haserror:
                print now(), fid, u'网页错误...', haserror
                return

            print now(), fid, u'填写卡号...'
            b.find_by_name('card_no').first.fill(card_no)
            b.find_by_name('sbmt').first.click()

            haserror = check_error(b)
            if haserror:
                print now(), fid, u'网页错误...', haserror
                return

            print now(), fid, u'填写名字,密码,电话...'
            b.find_by_name('password').first.fill(password)
            b.find_by_name('sei').first.fill(sei)
            b.find_by_name('mei').first.fill(mei)
            b.find_by_name('sei_kana').first.fill(sei_kana)
            b.find_by_name('mei_kana').first.fill(mei_kana)
            tel1, tel2, tel3 = tel.split('-')
            b.find_by_name('tel1').first.fill(tel1)
            b.find_by_name('tel2').first.fill(tel2)
            b.find_by_name('tel3').first.fill(tel3)
            b.find_by_name('sbmt').first.click()

            haserror = check_error(b)
            if haserror:
                print now(), fid, u'网页错误...', haserror
                return

            print now(), fid, u'再次最后确认...'
            b.find_by_name('sbmt').first.click()

            if haserror:
                print now(), fid, u'网页错误...', haserror
                return

            print now(), fid, u'抢购成功...'
            break
        time.sleep(1)


def main():
    data = xlrd.open_workbook('qianggou6.xls')
    table = data.sheets()[0]
    nrows = table.nrows
    threads = []
    for i in range(1, nrows):
        threads.append(BuyThread(table.row_values(i)))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()
    time.sleep(200)
