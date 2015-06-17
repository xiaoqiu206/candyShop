# coding=utf-8
'''
Created on 2015年5月27日

@author: Administrator
'''
import redis
import memcache
import sqlite3
import time
import datetime

# memcache常量
MEMCACHE_TIME_OUT = 120  # memcached 过期时间

TOKEN = 'jj24l5na090h2kq309ah2'  # php接口token值
# php处理订单的API的url
PHP_ORDER_URL = 'http://chuanmei.taotangmi.com/index.php?c=api&a=get_orders'
PHP_PRINTERS_STATUS_URL = 'http://chuanmei.taotangmi.com/index.php?c=api&a=get_printer_status&'

# 调用有赞API(查询卖家已卖出的交易列表)调用参数
YOUZAN_URL = 'http://open.koudaitong.com/api/entry'
YOUZAN_START_TIME = 100  # 获取100秒内的订单

# FEIE打印机接口调用参数
FEIE_HOST = ''
FEIE_QUERY_PRINTER_STATUS_ACTION = '/queryPrinterStatusAction'

# redis连接
_REDIS_CONNECTION = None


def get_redis_con():
    global _REDIS_CONNECTION
    'redis连接(单例模式)'
    if _REDIS_CONNECTION:
        return _REDIS_CONNECTION
    # redis连接参数
    host = ''
    port = 6379
    user = ''
    pwd = ''
    pool = redis.ConnectionPool(
        host=host, port=port, password=user + ':' + pwd)
    _REDIS_CONNECTION = redis.Redis(connection_pool=pool)
    return _REDIS_CONNECTION

# memcache
_MEMCACHE_CONNECTION = None


def get_memcache_con():
    global _MEMCACHE_CONNECTION
    'memcache连接(单例模式)'
    if _MEMCACHE_CONNECTION:
        return _MEMCACHE_CONNECTION
    _MEMCACHE_CONNECTION = memcache.Client(['127.0.0.1:11211'])
    return _MEMCACHE_CONNECTION


def sqlite_log(event, local_data, push_data=None, response_status=None, response_data=None):
    try:
        con = sqlite3.connect('log.db')
        cur = con.cursor()
        data = (event, local_data, str(push_data), str(
            response_status), str(response_data))
        cur.execute(
            "insert into log(event,local_data,push_data,response_status,response_data)values(?,?,?,?,?)", data)
    except Exception, e:
        print TimeUtils.get_timestamp(), 'function sqlite_log', e
    con.commit()
    con.close()


class TimeUtils():

    '一些获取格式化时间的工具方法'
    @staticmethod
    def get_timestamp():
        '返回格式化的时间戳'
        return time.strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def get_start_created():
        '有赞接口开始交易时间'
        some_time_ago = datetime.datetime.now(
        ) - datetime.timedelta(seconds=YOUZAN_START_TIME)
        some_time_ago_format = some_time_ago.strftime('%Y-%m-%d %H:%M:%S')
        return some_time_ago_format
