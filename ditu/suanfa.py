# coding=utf-8
'''
Created on 2016年1月16日
第一版,不考虑4号线和2号线换乘方便
@author: xiaoq
'''
import pymysql

from itertools import permutations

DB_HOST = '127.0.0.1'
DB_PORT = 3306
DB_USER = 'root'
DB_PASSWORD = '123321'
DB_NAME = 'whrt'

SELECT_STATION_SQL = """select
                station_id,
                station_num,
                station_name,
                line_id,
                is_transfer,
                sequence
          from STATIONS;"""


def find_shortest_path(graph, start, end, path=[]):
    '''找到图的最短路径算法'''
    path = path + [start]
    if start == end:
        return path
    if not graph.has_key(start):
        return None
    shortest = None
    for node in graph[start]:
        if node not in path:
            newpath = find_shortest_path(graph, node, end, path)
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
    return shortest


class Station(object):
    """站点类,用来存储每个站点的信息,每个属性映射到STAIONS表的一个字段
    int sid: 映射字段STATION_ID 站点id,
    int snum: 映射字段STATION_NUM 站点编号,
    str sname: 映射字段STATION_NAME 站点名称
    int line_id: 映射字段LINE_ID 线路号,例如3号线,4号线
    int is_transfer: 映射字段IS_TRANSFER 是否为换乘站
    int sequence: 映射字段SEQUENCE 站点排序字段,
    """

    def __init__(self, sid, snum, sname, line_id, is_transfer, sequence):
        self.sid = sid
        self.snum = snum
        self.sname = sname
        self.line_id = line_id
        self.is_transfer = is_transfer
        self.sequence = sequence

    def __str__(self):
        line = '%s号线' % self.line_id \
            if not self.is_transfer \
            else '换乘站(%s,%s)' % self.line_id
        return '%s:  %s' % (self.sname, line)

    def __repr__(self):
        line = '换乘站(%s,%s)' % self.line_id \
            if self.is_transfer \
            else '%s号线' % self.line_id
        return '%s:  %s' % (self.sname.encode('utf-8'), line)


def get_stations():
    con = pymysql.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME, charset='gbk')
    cur = con.cursor()
    cur.execute(SELECT_STATION_SQL)
    rows = cur.fetchall()
    stations = []
    for sid, snum, sname, line_id, is_transfer, sequence in rows:
        stations.append(Station(
            sid, str(snum), sname, str(line_id), is_transfer, sequence))
    return stations


def stations2tu(stations):
    tu = {}
    for station in stations:
        snum = station.snum
        sequence = station.sequence
        close_sequences = (sequence + 1, sequence - 1)
        line_id = station.line_id
        close_stations = [
            each.snum for each in stations if each.sequence in close_sequences and each.line_id == line_id]
        if (not station.is_transfer) or (snum not in tu):
            tu[snum] = close_stations
        else:
            # 中南路和洪山广场,特殊情况去重
            tu[snum] = list(set(tu[snum] + close_stations))
    return tu


def main():
    tu = stations2tu(stations)
    # pprint(snums)
    # print len(snums)  # 96个站,有6个是换乘站
    start_ends = permutations(snums, 2)
    f = open('luxian3.txt', 'w')
    for start, end in start_ends:
        short_path = find_shortest_path(tu, start, end)
        line_ids = []
        for cross_station_num in short_path:
            if not snum_stations[cross_station_num].is_transfer:
                line_ids.append(snum_stations[cross_station_num].line_id)
        line_ids = ''.join(line_ids)
        if '24' in line_ids or '42' in line_ids:  # 如果有4号线和2号线换乘
            pass
        else:
            print start, '-', end, ' 线路:'
            for cross_station_num in short_path:
                print ''
        '''
        f.write(snum_stations[start].sname + '-' +
                snum_stations[end].sname + ' 路线: ')
        for each in short_path:
            f.write(snum_stations[each].sname + '-')
        f.write('\n')
        '''
    f.close()

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    stations = get_stations()
    snums = list(set([station.snum for station in stations]))
    snum_stations = {station.snum: station for station in stations}
    main()
