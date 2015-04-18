# coding=utf-8
'''
Created on 2015年3月28日
赌球,数据分析
@author: Administrator
'''
import tkFont
from Tkinter import Tk, Frame, Label, Button, Text, END
import urllib
import xlwt
from bs4 import BeautifulSoup
import time


root = Tk()
ft = tkFont.Font(size=12)
label1 = Label(root, font=ft, text='输入网址(结尾不要带ctype=1):')
label1.pack()

zy_list = []
zy_data = []


def baifenshu(str1):
    return str(float(str1.replace('%', '')) / 100)[0:5]


def excel():
    # 判断是不是有9个
    length = len(label2['text'].split('||'))
    if length != 10:
        label3['text'] = u'你输入了' + str(length - 1) + u'公司'
        return
    ef = xlwt.Workbook(encoding='utf-8')
    table = ef.add_sheet('sheet1')

    # 获取选定的主流公司的数据写入右边区域
    url = entry1.get('0.0', END)
    fullurl = url + '?ctype=2'
    print '获取到的主流公司url', url
    # html = urllib.urlopen(url + '?ctype=2').read()  # 获取主流公司

    soup = BeautifulSoup(open('2.html'), 'html5lib')
    trs = soup.find_all('tr', id=True)
    want_list = label2['text'].split(':')[1].split('||')
    global zy_data
    for each in trs:
        if each.find_all('td', limit=2)[1].find('p').find('a').find('span').get_text() in want_list:
            tbody = each.find_all('td')[2].find('table').find('tbody')
            for x in range(0, 2):
                for y in range(0, 3):
                    zy_data.append(tbody.find_all('tr')[x].find_all('td')[y].get_text())
    # print zy_data
    length = len(zy_data)
    # 设置背景颜色深黄
    styleGray = xlwt.easyxf("font: height 240, name Arial; align: wrap on, vert centre, horiz center;"'pattern:pattern solid,fore_color gray25')
    i = 0
    for x in range(1, length / 6 + 1):
        for y in range(10, 16):
            table.write(x, y, zy_data[i], styleGray)
            i += 1
    # 以上是主流公司
    # 下面是平均值
    avgList = []
    btm = soup.find(id='table_btm')
    for x in range(0, 6):
        avgList.append(btm.find('table').find('tbody').find_all('td')[x])
    i = 0
    styleLightYellow = xlwt.easyxf("font: height 240, name Arial; align: wrap on, vert centre, horiz center;"'pattern:pattern solid,fore_color light_yellow')
    for y in range(10, 16):
        table.write(0, y, avgList[i].get_text(), styleLightYellow)
        i += 1

    # 下面是粉色数据
    pinkList = []
    pinkList.append(baifenshu(btm.find('table').find_all('tbody')[2].find_all('td')[0].get_text()))
    for x in range(0, 3):
        pinkList.append(btm.find('table').find_all('tbody')[3].find_all('td')[x].get_text())
    pinkList.append(baifenshu(btm.find('table').find_all('tbody')[2].find_all('td')[1].get_text()))
    for x in range(3, 6):
        pinkList.append(btm.find('table').find_all('tbody')[3].find_all('td')[x].get_text())
    pinkList.append(baifenshu(btm.find('table').find_all('tbody')[6].find_all('td')[0].get_text()))
    for x in range(0, 3):
        pinkList.append(btm.find('table').find_all('tbody')[7].find_all('td')[x].get_text())
    pinkList.append(baifenshu(btm.find('table').find_all('tbody')[6].find_all('td')[1].get_text()))   
    for x in range(3, 6):
        pinkList.append(btm.find('table').find_all('tbody')[7].find_all('td')[x].get_text())
    pinkList.append(baifenshu(btm.find('table').find_all('tbody')[10].find_all('td')[0].get_text()))
    for x in range(0, 3):
        pinkList.append(btm.find('table').find_all('tbody')[11].find_all('td')[x].get_text())
    pinkList.append(baifenshu(btm.find('table').find_all('tbody')[10].find_all('td')[1].get_text()))
    for x in range(3, 6):
        pinkList.append(btm.find('table').find_all('tbody')[11].find_all('td')[x].get_text())
    # print pinkList
    # 粉色数据
    i = 0
    stylePink = xlwt.easyxf("font: height 240, name Arial; align: wrap on, vert centre, horiz center;"'pattern:pattern solid,fore_color pink')
    for x in (1, 2, 4, 5, 7, 8):
        for y in range(0, 4):
            table.write(x, y, pinkList[i], stylePink)
            i += 1

    # 交易所的平均值
    soup = BeautifulSoup(open('3.html'))
    pinkList = []
    btm = soup.find(id='table_btm')
    pinkList.append(baifenshu(btm.find('table').find_all('tbody')[2].find_all('td')[0].get_text()))
    for x in range(0, 3):
        pinkList.append(btm.find('table').find_all('tbody')[3].find_all('td')[x].get_text())
    pinkList.append(baifenshu(btm.find('table').find_all('tbody')[2].find_all('td')[1].get_text()))
    for x in range(3, 6):
        pinkList.append(btm.find('table').find_all('tbody')[3].find_all('td')[x].get_text())
    pinkList.append(baifenshu(btm.find('table').find_all('tbody')[6].find_all('td')[0].get_text()))
    for x in range(0, 3):
        pinkList.append(btm.find('table').find_all('tbody')[7].find_all('td')[x].get_text())
    pinkList.append(baifenshu(btm.find('table').find_all('tbody')[6].find_all('td')[1].get_text()))   
    for x in range(3, 6):
        pinkList.append(btm.find('table').find_all('tbody')[7].find_all('td')[x].get_text())
    pinkList.append(baifenshu(btm.find('table').find_all('tbody')[10].find_all('td')[0].get_text()))
    for x in range(0, 3):
        pinkList.append(btm.find('table').find_all('tbody')[11].find_all('td')[x].get_text())
    pinkList.append(baifenshu(btm.find('table').find_all('tbody')[10].find_all('td')[1].get_text()))
    for x in range(3, 6):
        pinkList.append(btm.find('table').find_all('tbody')[11].find_all('td')[x].get_text())
    # print pinkList
    # 蓝色色数据
    i = 0
    styleGreen = xlwt.easyxf("font: height 240, name Arial; align: wrap on, vert centre, horiz center;"'pattern:pattern solid,fore_color green')
    for x in (10, 11, 13, 14, 16, 17):
        for y in range(0, 4):
            table.write(x, y, pinkList[i], styleGreen)
            i += 1
    # 红色离散值
    redList = []
    for x in range(0, 6):
        redList.append(btm.find('table').find_all('tbody')[12].find_all('td')[x])
    i = 0
    styleRed = xlwt.easyxf("font: height 240, name Arial; align: wrap on, vert centre, horiz center;"'pattern:pattern solid,fore_color red')
    for x in range(1, 3):
        for y in range(4, 7):
            table.write(x, y, redList[i].get_text(), styleRed)
            i += 1
    fname = unicode(soup.title.get_text()) + u'.xls'
    table.write_merge(0, 0, 1, 9, soup.title.get_text(), xlwt.easyxf("font: height 240, name Arial; align: wrap on, vert centre, horiz center;"))
    ef.save(fname.replace('/', '-'))


def sure():
    """
    爬取网站上的主流公司列表
    """
    url = entry1.get('0.0', END)
    # html = urllib.urlopen(url + '?ctype=2').read()  # 获取主流公司
    soup = BeautifulSoup(open('2.html'))
    trs = soup.find_all('tr', id=True)
    global zy_list
    for each in trs:
        zy_list.append(each.find_all('td', limit=2)[1].find('p').find('a').find('span').get_text())
    print zy_list 
    exeBtn()

def exeBtn():
    for _, btn in frame1.children.items():
        if btn['text'] not in zy_list:
            btn['state'] = 'disabled'
ft1 = tkFont.Font(size=15)
entry1 = Text(root, width=80, height=2, font=ft1)
entry1.pack()
frame = Frame(root)
frame.pack()


def reset():
    label3['text'] = ''
    for k, v in frame1.children.items():
        v['state'] = 'normal'
    label2['text'] = u'选中的公司有:'
    global zy_list
    zy_list = []
    global zy_data
    zy_data = []
    entry1.delete(0.0, END)

Button(frame, text='获取有效的公司', command=sure, font=ft).grid(row=0, column=0)
Button(frame, text='生成excel', command=excel, font=ft).grid(row=0, column=2)
Button(frame, text='重置', command=reset, font=ft).grid(row=0, column=4)
label3 = Label(frame, text='')
label3.grid(row=0, column=6)
frame1 = Frame(root, width=120)
frame1.pack()

list1 = [u'竞彩官方', u'威廉希尔', u'澳门', u'Ladbrokes (立博)', u'Bet365']


def f1():
    if list1[0] in label2['text']:
        label2['text'] = label2['text'].replace(list1[0] + '||', '')
    else:
        label2['text'] = label2['text'] + list1[0] + '||'

Button(frame1, text=list1[0], width=20, command=f1).grid(column=0, row=0)


def f2():
    if list1[1] in label2['text']:
        label2['text'] = label2['text'].replace(list1[1] + '||', '')
    else:
        label2['text'] = label2['text'] + list1[1] + '||'
Button(frame1, text=list1[1], width=20, command=f2).grid(column=1, row=0)


def f3():
    if list1[2] in label2['text']:
        label2['text'] = label2['text'].replace(list1[2] + '||', '')
    else:
        label2['text'] = label2['text'] + list1[2] + '||'
Button(frame1, text=list1[2], width=20, command=f3).grid(column=2, row=0)


def f4():
    if list1[3] in label2['text']:
        label2['text'] = label2['text'].replace(list1[3] + '||', '')
    else:
        label2['text'] = label2['text'] + list1[3] + '||'
Button(frame1, text=list1[3], width=20, command=f4).grid(column=3, row=0)


def f5():
    if list1[4] in label2['text']:
        label2['text'] = label2['text'].replace(list1[4] + '||', '')
    else:
        label2['text'] = label2['text'] + list1[4] + '||'
Button(frame1, text=list1[4], width=20, command=f5).grid(column=4, row=0)

list2 = [u'Interwetten (英特)', u'SNAI', u'Singbet (皇冠)', u'Easybets (易胜博)', u'BetVictor (伟德)']


def f6():
    if list2[0] in label2['text']:
        label2['text'] = label2['text'].replace(list2[0] + '||', '')
    else:
        label2['text'] = label2['text'] + list2[0] + '||'
Button(frame1, text=list2[0], width=20, command=f6).grid(column=0, row=1)


def f7():
    if list2[1] in label2['text']:
        label2['text'] = label2['text'].replace(list2[1] + '||', '')
    else:
        label2['text'] = label2['text'] + list2[1] + '||'
Button(frame1, text=list2[1], width=20, command=f7).grid(column=1, row=1)


def f8():
    if list2[2] in label2['text']:
        label2['text'] = label2['text'].replace(list2[2] + '||', '')
    else:
        label2['text'] = label2['text'] + list2[2] + '||'
Button(frame1, text=list2[2], width=20, command=f8).grid(column=2, row=1)


def f9():
    if list2[3] in label2['text']:
        label2['text'] = label2['text'].replace(list2[3] + '||', '')
    else:
        label2['text'] = label2['text'] + list2[3] + '||'
Button(frame1, text=list2[3], width=20, command=f9).grid(column=3, row=1)


def f10():
    if list2[4] in label2['text']:
        label2['text'] = label2['text'].replace(list2[4] + '||', '')
    else:
        label2['text'] = label2['text'] + list2[4] + '||'
Button(frame1, text=list2[4], width=20, command=f10).grid(column=4, row=1)

list3 = [u'Oddset (奥德赛特)', u'Bwin (必赢)', u'Gamebookers', u'PinnacleSports (平博)', u'10BET']


def f11():
    if list3[0] in label2['text']:
        label2['text'] = label2['text'].replace(list3[0] + '||', '')
    else:
        label2['text'] = label2['text'] + list3[0] + '||'
Button(frame1, text=list3[0], width=20, command=f11).grid(column=0, row=2)


def f12():
    if list3[1] in label2['text']:
        label2['text'] = label2['text'].replace(list3[1] + '||', '')
    else:
        label2['text'] = label2['text'] + list3[1] + '||'
Button(frame1, text=list3[1], width=20, command=f12).grid(column=1, row=2)


def f13():
    if list3[2] in label2['text']:
        label2['text'] = label2['text'].replace(list3[2] + '||', '')
    else:
        label2['text'] = label2['text'] + list3[2] + '||'
Button(frame1, text=list3[2], width=20, command=f13).grid(column=2, row=2)


def f14():
    if list3[3] in label2['text']:
        label2['text'] = label2['text'].replace(list3[3] + '||', '')
    else:
        label2['text'] = label2['text'] + list3[3] + '||'
Button(frame1, text=list3[3], width=20, command=f14).grid(column=3, row=2)


def f15():
    if list3[4] in label2['text']:
        label2['text'] = label2['text'].replace(list3[4] + '||', '')
    else:
        label2['text'] = label2['text'] + list3[4] + '||'
Button(frame1, text=list3[4], width=20, command=f15).grid(column=4, row=2)


list4 = [u'Coral', u'Sbobet (利记)', u'Unibet (优胜客)', u'SportingBet (博天堂)', u'Mansion88 (明升)']


def f16():
    if list4[0] in label2['text']:
        label2['text'] = label2['text'].replace(list4[0] + '||', '')
    else:
        label2['text'] = label2['text'] + list4[0] + '||'
Button(frame1, text=list4[0], width=20, command=f16).grid(column=0, row=3)


def f17():
    if list4[1] in label2['text']:
        label2['text'] = label2['text'].replace(list4[1] + '||', '')
    else:
        label2['text'] = label2['text'] + list4[1] + '||'
Button(frame1, text=list4[1], width=20, command=f17).grid(column=1, row=3)


def f18():
    if list4[2] in label2['text']:
        label2['text'] = label2['text'].replace(list4[2] + '||', '')
    else:
        label2['text'] = label2['text'] + list4[2] + '||'
Button(frame1, text=list4[2], width=20, command=f18).grid(column=2, row=3)


def f19():
    if list4[3] in label2['text']:
        label2['text'] = label2['text'].replace(list4[3] + '||', '')
    else:
        label2['text'] = label2['text'] + list4[3] + '||'
Button(frame1, text=list4[3], width=20, command=f19).grid(column=3, row=3)


def f20():
    if list4[4] in label2['text']:
        label2['text'] = label2['text'].replace(list4[4] + '||', '')
    else:
        label2['text'] = label2['text'] + list4[4] + '||'
Button(frame1, text=list4[4], width=20, command=f20).grid(column=4, row=3)

list5 = [u'188Bet (金宝博)', u'香港马会', u'Eurobet (欧博)', u'UEDBET (UED亚洲)', u'18luck (新利)']


def f21():
    if list5[0] in label2['text']:
        label2['text'] = label2['text'].replace(list5[0] + '||', '')
    else:
        label2['text'] = label2['text'] + list5[0] + '||'
Button(frame1, text=list5[0], width=20, command=f21).grid(column=0, row=4)


def f22():
    if list5[1] in label2['text']:
        label2['text'] = label2['text'].replace(list5[1] + '||', '')
    else:
        label2['text'] = label2['text'] + list5[1] + '||'
Button(frame1, text=list5[1], width=20, command=f22).grid(column=1, row=4)


def f23():
    if list5[2] in label2['text']:
        label2['text'] = label2['text'].replace(list5[2] + '||', '')
    else:
        label2['text'] = label2['text'] + list5[2] + '||'
Button(frame1, text=list5[2], width=20, command=f23).grid(column=2, row=4)


def f24():
    if list5[3] in label2['text']:
        label2['text'] = label2['text'].replace(list5[3] + '||', '')
    else:
        label2['text'] = label2['text'] + list5[3] + '||'
Button(frame1, text=list5[3], width=20, command=f24).grid(column=3, row=4)


def f25():
    if list5[4] in label2['text']:
        label2['text'] = label2['text'].replace(list5[4] + '||', '')
    else:
        label2['text'] = label2['text'] + list5[4] + '||'
Button(frame1, text=list5[4], width=20, command=f25).grid(column=4, row=4)

for k, v in frame1.children.items():
    v['width'] = 30
    v['height'] = 3

frame2 = Frame(root)
frame2.pack()

for k, v in frame1.children.items():
    v['font'] = ft
    v['width'] = 25


label2 = Label(frame2, font=ft, text='选中的公司有:', height=5)
label2.pack()
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

root.mainloop()
