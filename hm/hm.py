# coding=utf-8
'''
Created on 2015年5月1日
计算数据相似性
@author: Administrator
'''
import csv
from operator import itemgetter
import time
import sys


def hamming_distance(s1, s2):
    assert len(s1) == len(s2)
    return sum(ch1 != ch2 for ch1, ch2 in zip(s1, s2))


def mycmp(x, y):
    if x[1] > y[1]:
        return -1
    elif x[1] < y[1]:
        return 1
    else:
        if x[2] > y[2]:
            return -1
        elif x[2] < y[2]:
            return 1
        else:
            if len(x[0]) < len(y[0]):
                return -1
            elif len(x[0]) > len(y[0]):
                return 1
            else:
                return cmp(x[0], y[0])


def analysis(filenames, hm=2):
    '''
    分析数据并且输出为csv,filenames是要分析的文件数组,hm是设定的海明距离值,小于这个值的数据将会编号
    '''
    data = []  # 存放合并后的数据
    for filename in filenames:
        reader = csv.reader(open(filename, 'rb'))
        rows = []  # 存放一个CSV的数据
        for row in reader:
            row.append(filename)
            row.append('')
            rows.append(row)
        firstrow = rows.pop(0)  # 删除行首数据
        data.extend(rows)
    firstrow[-1] = 'hm'  # 行首倒数第一列为hm
    firstrow[-2] = 'csv'  # 行首倒数第二列为csv
    data.sort(cmp=mycmp)
    # data.sort(key=itemgetter(1, 2))  # 排序

    length = len(data)
    print u'数据总行数: ', length
    # print data[0:300]
    count = 1  # 编号
    for k, v in enumerate(data):
        if k % 10000 == 0:
            print k, time.strftime("%H:%M:%S", time.localtime(time.time()))
        # 先和前一个数据比对,如果和前一个数据A,B,C列相同将不比对
        if k > 0 and v[0] == data[k - 1][0] and v[1] == data[k - 1][1] and v[2] == data[k - 1][2]:
            v[-1] = data[k - 1][-1]
            continue
        for x in xrange(k + 1, length):  # 遍历后面每行,比对数据
            if v[1] + v[2] == data[x][1] + data[x][2]:  # 如果BC列相同,就比对A列
                # 如果A列长度相同并且海明距离小于等于设定数值,就添加编号
                if len(v[0]) == len(data[x][0]):
                    if hamming_distance(v[0], data[x][0]) <= hm:
                        data[x][-1] += str(count) + ' '
                        v[-1] += str(count) + ' '
                        count += 1
                else:  # 如果A列长度不一样,就结束本次循环,后面的不用比对
                    break
            else:  # 如果BC列不相同,那么后面的就不用比对了,本次循环结束
                break
    f1 = file('3.csv', 'wb')
    
    # 全部数据写入一个CSV分析
    writer = csv.writer(f1)
    for each in data:
       writer.writerow(each) 

    # 将数据转化为字典,格式为 csv文件名:数据
    datadict = {}
    for each in data:
        if each[-2] in datadict:
            datadict[each[-2]].append(each)
        else:
            datadict[each[-2]] = []
            datadict[each[-2]].append(each)
    firstrow.pop(-2)  # 将行首的csv列删除
    # 写入csv
    for k, v in datadict.iteritems():
        newfile = file(k.split('.')[0] + '-hm-' + str(hm) + '.csv', 'wb')
        writer = csv.writer(newfile)
        writer.writerow(firstrow)
        v.sort(key=itemgetter(0, 1, 2))
        for each in v:
            each.pop(-2)
            writer.writerow(each)
        newfile.close()


if __name__ == '__main__':
    filenames = ('411.csv', '426.csv', '520.csv', '55.csv', '625.csv')
    print u'开始时间', time.strftime("%H:%M:%S", time.localtime(time.time()))
    if len(sys.argv) > 1:
        hm = int(sys.argv[1])
        print u'设置的数字是: ', hm
        analysis(filenames, hm)
    else:
        print u'没有设置数字,使用默认数字'
        analysis(filenames)
    print u'结束时间', time.strftime("%H:%M:%S", time.localtime(time.time()))
