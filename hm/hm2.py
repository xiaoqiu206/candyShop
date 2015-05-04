# coding=utf-8
'''
Created on 2015年5月1日
计算数据相似性,备份2
@author: Administrator
'''
import csv
from operator import itemgetter
import time


def hamming_distance(s1, s2):
    assert len(s1) == len(s2)
    return sum(ch1 != ch2 for ch1, ch2 in zip(s1, s2))


def analysis(filenames, hm):
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
    data.sort(key=itemgetter(1, 2))  # 排序
    
    sortdata = []
    
    
    
    
    length = len(data)
    for k, v in enumerate(data):
        if k % 10000 == 0:
            print k, time.strftime("%H:%M:%S", time.localtime(time.time()))
        v[-1] += str(k) + ' '  # 给每行编号
        for x in xrange(k + 1, length):  # 遍历后面每行,比对数据
            if len(v[0]) == len(data[x][0]):
                if v[1] == data[x][1] and v[2] == data[x][2]:
                    pass
                else:
                    break
            else:
                break
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
    analysis(filenames, hm=2)
    print u'结束时间', time.strftime("%H:%M:%S", time.localtime(time.time()))
