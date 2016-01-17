# coding=utf-8
'''
Created on 2016年1月16日
需要考虑2号线和4号线的换乘,在中南路换乘最方便
@author: xiaoq
'''
import pymysql

from pprint import pprint
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


def find_all_paths(graph, start, end, path=[]):
    '''找到图的所有路径算法'''
    path = path + [start]
    if start == end:
        return [path]
    if not graph.has_key(start):
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = find_all_paths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths


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
    str line_id: 映射字段LINE_ID 线路号,例如3号线,4号线
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
    f = open('luxian1.txt', 'w')
    for start, end in start_ends:
        # 如果2个站点在一条线路上,就直接用最短路径算法,节省时间和空间
        # 将start和end所在线路全部存到一个列表里,如果有重复,就是在同一线路
        line_ids = [
            station.line_id for station in stations if station.snum in (start, end)]
        length1 = len(line_ids)
        length2 = len(set(line_ids))
        if length2 < length1:
            short_path = find_shortest_path(tu, start, end)
        else:
            # 先算出所有路径
            all_path = find_all_paths(tu, start, end)
            # 最短路径的长度
            min_len = min([len(path) for path in all_path])
            # 筛选出所有的最短路径
            all_short_path = filter(
                lambda path: len(path) == min_len, all_path)
            if len(all_short_path) == 1:
                # 如果最短路径方案只有一个,就直接使用这个
                short_path = all_short_path[0]
            else:
                # 如果没有2号线和4号线换乘,随机选一条
                # 如果有2号线和4号线换乘,就选择在中南路换乘的线路
                for path in all_short_path:
                    break_flag = 0
                    if break_flag:
                        break
                    # 先计算出路径都走了几号线
                    line_ids = []
                    for cross_snum in path:
                        if not snum_stations[cross_snum].is_transfer:
                            line_ids.append(snum_stations[cross_snum].line_id)
                    line_ids = ''.join(line_ids)
                    if line_ids.find('24') > -1 or line_ids.find('42') > -1:
                        # 如果有2号线和4号线换乘,选择在中南路换乘
                        for cross_snum in path:
                            if cross_snum == '44':  # 中南路的stataion_num是44
                                short_path = path
                                break_flag = 1
                                break
                    else:
                        # 如果没有2号线和4号线换乘,随机选择一条
                        short_path = path
                        break

        f.write(snum_stations[start].sname + '-' +
                snum_stations[end].sname + u' 路线: ')
        for each in short_path:
            f.write(snum_stations[each].sname + '-')
        f.write('\n')
    f.close()

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    stations = get_stations()
    snums = list(set([station.snum for station in stations]))
    snum_stations = {station.snum: station for station in stations}
    main()
