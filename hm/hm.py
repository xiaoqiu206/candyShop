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


def get_now():
    '''
    返回现在的格式化时间
    '''
    return time.strftime("%H:%M:%S", time.localtime(time.time()))


def hamming_distance(s1, s2):
    '''
        计算2个字符串的海明距离
    '''
    assert len(s1) == len(s2)
    return sum(ch1 != ch2 for ch1, ch2 in zip(s1, s2))


def mycmp(x, y):
    '''
    排序方法,先比较1,2列是否相同,如果相同,再比较0列的长度
    '''
    if x[1] < y[1]:
        return -1
    elif x[1] > y[1]:
        return 1
    else:
        if x[2] < y[2]:
            return -1
        elif x[2] > y[2]:
            return 1
        else:
            if len(x[0]) < len(y[0]):
                return -1
            elif len(x[0]) > len(y[0]):
                return 1
            else:
                return cmp(x[0], y[0])


def toDict(data):
    '''
    将列表转为字典,key为列表中的csv文件名
    '''
    datadict = {}
    for each in data:
        if each[-2] in datadict:
            datadict[each[-2]].append(each)
        else:
            datadict[each[-2]] = []
            datadict[each[-2]].append(each)
    return datadict


def toCSV(datadict, firstrow, hm):
    '''
    将字典输出为CSV文件
    '''
    for k, v in datadict.iteritems():
        newfile = file(k.split('.')[0] + '-hm-' + str(hm) + '.csv', 'wb')
        writer = csv.writer(newfile)
        writer.writerow(firstrow)
        v.sort(key=itemgetter(0, 1, 2))
        for each in v:
            each.pop(-2)
            writer.writerow(each)
        newfile.close()


# 将数据写入excel
def toExcel(data, filename):
    f1 = file(filename, 'wb')
    writer = csv.writer(f1)
    for each in data:
        writer.writerow(each)


def handler_data(data, hm):
    '''
    比对列表中的数据,海默距离小于hm的,赋值相同的编号
    '''
    length = len(data)
    count = 1  # 编号
    for k, v in enumerate(data):
        v[-1] += str(count) + ' '
        if k % 10000 == 0:
            print k, time.strftime("%H:%M:%S", time.localtime(time.time()))
        # 先和前一个数据比对,如果和前一个数据A,B,C列相同将不比对
        if k > 0 and (v[0], v[1], v[2]) == (data[k - 1][0], data[k - 1][1], data[k - 1][2]):
            v[-1] = data[k - 1][-1]
            continue
        for x in xrange(k + 1, length):  # 遍历后面每行,比对数据
            # 如果BC列相同且A列长度相同,就计算海明距离
            if (v[1], v[2]) == (data[x][1], data[x][2]) and len(v[0]) == len(data[x][0]):
                if hamming_distance(v[0], data[x][0]) <= hm:
                    data[x][-1] += str(count) + ' '
            else:  # 如果BC列不相同,那么后面的就不用比对了,本次循环结束
                break
        count += 1
    for each in data:
        if each[-1] == '':
            count += 1
            each[-1] = count
    print count

def analysis(filenames, hm=2):
    '''
    分析数据并且输出为csv,filenames是要分析的文件数组,hm是设定的海明距离值,小于这个值的数据将会编号
    '''
    data = []  # 存放合并后的数据
    for filename in filenames:  # 将所有CSV文件里的数据存到一个列表里
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
    length = len(data)
    print u'数据总行数: ', length
    # print data[0:300]
    handler_data(data, hm)  # 比对数据的海默距离,并且编号
    toExcel(data, '1.csv')  # 将编号后的列表输出为csv,以便分析
    datadict = toDict(data)  # 将数据转化为字典,格式为 csv文件名:数据
    firstrow.pop(-2)  # 将行首的csv列删除
    toCSV(datadict, firstrow, hm)  # 写入csv


if __name__ == '__main__':
    filenames = ('411.csv', '426.csv', '520.csv', '55.csv', '625.csv')
    print u'开始时间', get_now()
    if len(sys.argv) > 1:
        hm = int(sys.argv[1])
        print u'设置的数字是: ', hm
        analysis(filenames, hm)
    else:
        print u'没有设置数字,使用默认数字'
        analysis(filenames)
    print u'结束时间', get_now()
