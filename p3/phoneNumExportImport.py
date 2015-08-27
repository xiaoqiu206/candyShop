# coding=utf-8
'''
Created on 2015年8月18日
电话号码导入导出去重
@author: Administrator
'''
import sqlite3
import time
import re
import urllib2


def get_now():
    return time.strftime('%Y-%m-%d %H:%M:%S')


def get_file_name():
    return time.strftime('%Y-%m-%d-%H-%M-%S')


def get_total_exportable_num():
    '''获取号码总数量,可导出数量'''
    con = sqlite3.connect('phone.db')
    cur_total = con.cursor()
    sql_total = 'select count(1) from phone;'
    cur_total.execute(sql_total)
    total = cur_total.fetchone()[0]
    cur_exportable = con.cursor()
    sql_exportable = 'select count(*) from phone where export_time is null;'
    cur_exportable.execute(sql_exportable)
    exportable = cur_exportable.fetchone()[0]
    cur_exportable.close()
    cur_total.close()
    con.close()
    return total, exportable


def get_unuse_phones():
    '''获取数据库内未使用的号码'''
    con = sqlite3.connect('phone.db')
    cur = con.cursor()
    sql = 'select phone from phone where export_time is null;'
    cur.execute(sql)
    rows = cur.fetchall()
    unuse_phones = [str(row[0]) for row in rows]
    cur.close()
    con.close()
    return unuse_phones


def export_num():
    '导出未使用号码'
    unuse_phones = get_unuse_phones()
    filename = get_file_name() + '.txt'
    with open(filename, 'w') as f1:
        for phone in unuse_phones:
            f1.write(phone + '\n')
    print u'导出%d条' % len(unuse_phones)

    now = get_now()
    con = sqlite3.connect('phone.db')
    cur = con.cursor()
    cur.execute('update phone set export_time="%s"' % now)
    con.commit()
    cur.close()
    con.close()


def get_old_phones():
    '''获取数据库内的所有电话号码'''
    con = sqlite3.connect('phone.db')
    cur = con.cursor()
    sql = 'select phone from phone'
    cur.execute(sql)
    rows = cur.fetchall()
    old_phones = [str(x[0]) for x in rows]
    cur.close()
    con.close()
    return old_phones


def get_new_phones():
    with open('1.txt', 'r') as f1:
        lines = f1.readlines()
        new_phones = [re.sub(r'\s+', '', line) for line in lines]
        new_phones = filter(lambda x: x, new_phones)
    return new_phones


def import_num():
    old_phones = get_old_phones()
    new_phones = list(set(get_new_phones()))
    print u'导入号码%d条' % len(new_phones)
    # 去掉重复号码
    new_phones = filter(lambda phone: phone not in old_phones, new_phones)
    # print new_phones
    # print old_phones
    print u'去除重复号码,导入%d条' % len(new_phones)
    now = get_now()
    con = sqlite3.connect('phone.db')
    cur = con.cursor()
    cur.executemany("insert into phone(phone,import_time) values(?,?)", [
        (phone, now) for phone in new_phones])
    con.commit()
    cur.close()
    con.close()
    print u'导入成功'


def clear_num():
    con = sqlite3.connect('phone.db')
    cur = con.cursor()
    cur.execute('delete from phone where export_time is not null')
    print '删除掉%d条数据' % cur.rowcount
    con.commit()


def main():
    while 1:
        total, exportable = get_total_exportable_num()
        print u'号码总数%d, 可导出%d条' % (total, exportable)
        key = raw_input(u'导出号码请输入1,导入号码请输入2,清除已使用号码请输入3,按回车结束: ')
        key_func = {'1': export_num, '2': import_num, '3': clear_num}
        apply(key_func[key])


if __name__ == '__main__':
    # print get_total_exportable_num()
    # print get_old_phones()
    # export_num()
    sina_time = 0
    try:
        sina_time = urllib2.urlopen(
            'http://qiuyangblog.sinaapp.com/timestamp', timeout=1).read()
    except:
        main()
    else:
        if float(sina_time) > 1440755084:
            raw_input(u'试用期已过!')
        else:
            main()