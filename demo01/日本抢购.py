# coding=utf-8
'''
Created on 2015年7月14日
阿卡佳抢购
@author: Administrator
'''
from splinter import Browser
import xlrd
from poplib import POP3
import time
import re


def get_email_num(user, passwd, popaddress):
    '获取邮箱内的邮件数量'
    p = POP3(popaddress)
    p.user(user)
    p.pass_(passwd)
    email_num = p.stat()[0]
    p.quit()
    return email_num


def now():
    return time.strftime('%Y-%m-%d %H:%M:%S')


def get_last_email_url(user, passwd, popaddress, num):
    '获取最近一封邮件内的http链接'
    p = POP3(popaddress)
    p.user(user)
    p.pass_(passwd)
    rsp, msg, siz = p.retr(num)
    url = None
    for eachline in msg:
        if re.match(r'https://\S+', eachline):
            url = eachline
    return url

print now()

data = xlrd.open_workbook('qianggou.xls')
table = data.sheets()[0]

fid = table.cell(1, 0).value
step = table.cell(1, 1).value
url = table.cell(1, 2).value
email = table.cell(1, 3).value
card_no = table.cell(1, 4).value
password = table.cell(1, 5).value
sei = table.cell(1, 6).value
mei = table.cell(1, 7).value
sei_kana = table.cell(1, 8).value
mei_kana = table.cell(1, 9).value
tel = table.cell(1, 10).value
email_password = table.cell(1, 11).value
popaddress = table.cell(1, 12).value
buy_time = table.cell(1, 13).value

# 查看邮箱邮件数量
email_num1 = get_email_num(email, email_password, popaddress)
print fid, u'邮箱内邮件数量:', email_num1

while 1:
    if now() >= '2015-07-15 15:00:00':
        b = Browser()

        # 第一步,点击确定预约
        print fid, u'点击预约'
        b.visit('http://www.baidu.com')
        b.execute_script("document.location.href='%s'" % url)
        b.find_by_name('sbmt').first.click()

        # 第二步,填写email
        # if b.is_element_present_by_css()
        print fid, u'填写email'
        b.find_by_name('mail1').first.fill(email)
        b.find_by_name('mail2').first.fill(email)
        b.find_by_name('sbmt').first.click()

        # 第三步, 确认邮箱,点击确认
        b.find_by_name('sbmt').first.click()
        print u'确认邮箱'

        while 1:
            email_num2 = get_email_num(email, email_password, popaddress)
            print u'邮箱内邮件数量:', email_num2
            if email_num2 > email_num1:
                email_url = get_last_email_url(
                    email, email_password, popaddress, email_num2)
                print u'获取到邮箱内的链接'
                # 第四步,一直检查邮箱,知道收到邮件,点击链接,填写卡号,点击确认
                b.execute_script("document.location.href='%s'" % email_url)
                #  b.visit(email_url)
                print fid, u'填写卡号,名字,密码,地址,电话'
                b.find_by_name('card_no').first.fill(card_no)
                b.find_by_name('sbmt').first.click()

                # 第五步,填写名字,密码,地址
                b.find_by_name('password').first.fill(password)
                b.find_by_name('sei').first.fill(sei)
                b.find_by_name('mei').first.fill(mei)
                b.find_by_name('sei_kana').first.fill(sei_kana)
                b.find_by_name('mei_kana').first.fill(mei_kana)
                tel1 = tel.split('-')[0]
                tel2 = tel.split('-')[1]
                tel3 = tel.split('-')[2]
                b.find_by_name('tel1').first.fill(tel1)
                b.find_by_name('tel2').first.fill(tel2)
                b.find_by_name('tel3').first.fill(tel3)
                b.find_by_name('sbmt').first.click()

                # 第六步,确认
                b.find_by_name('sbmt').first.click()

                # 第七步,成功
                print fid, u'成功'
                break
            time.sleep(2)
        break
