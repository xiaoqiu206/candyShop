# coding=utf-8
'''
Created on 2015年5月12日
云打印,自动获取订单,使用了python-memcached包
@author: Administrator
'''
import MySQLdb
import time
import datetime
import hashlib
import urllib
import urllib2
import json
import threading
import thread
import memcache
import sqlite3


MEMCACHE_TIME_OUT = 3600  # memcached 过期时间
TOKEN = 'jj24l5na090h2kq309ah2'  # php接口token值
# php处理订单的API的url
PHP_ORDER_URL = 'http://chuanmei.taotangmi.com/index.php?c=api&a=get_orders'
PHP_PRINTERS_STATUS_URL = 'http://chuanmei.taotangmi.com/index.php?c=api&a=get_printer_status&'
DB_CONNECTION = None  # 数据库连接connection,做个长连接
TID_USERID_MC = None  # memcached,key=tid,value=user_id

# 阿里云数据库连接参数
DB_HOST = 'tangmi2015.mysql.rds.aliyuncs.com'
DB_PORT = 3306
DB_USER = 'printergiahoocom'
DB_PASSWORD = '231f5407'
DB_NAME = 'printergiahoocom'

# DB_HOST = '127.0.0.1'
# DB_PORT = 3306
# DB_USER = 'root'
# DB_PASSWORD = '123321'
# DB_NAME = 'printergiahoocom'

# SQL语句模板
# 获取user_id,app_id,app_secret
SQL_GET_APPID_SECRET = """
SELECT 
    user_id, 
    appid, 
    appsecert 
    FROM user_view 
"""
# 获取飞蛾打印机状态信息的SQL语句
SQL_GET_PRINT_STATUS = """
SELECT 
    printer_id, 
    printer_number,
    printer_key,
    printer_status,
    printer_info
FROM printer_view
WHERE printer_type = 'feie' and printer_exp_time > now();
"""

# 调用有赞API(查询卖家已卖出的交易列表)调用参数
YOUZAN_URL = 'http://open.koudaitong.com/api/entry'
# FEIE打印机接口调用参数
FEIE_HOST = 'http://121.42.48.187/WPServer'
FEIE_QUERY_PRINTER_STATUS_ACTION = '/queryPrinterStatusAction'


class OrderThread(threading.Thread):

    '读取商家订单'

    def __init__(self, user_id, app_id, app_secret):
        threading.Thread.__init__(self)
        self.user_id = user_id
        self.app_id = app_id
        self.app_secret = app_secret

    def run(self):
        get_orders(self.user_id, self.app_id, self.app_secret, 1)


def update_printer_status(print_id, number, key, status, info):
    new_status, new_info = get_new_printer_status(number, key)
    if status != new_status or info != new_info:
        data = {'token': TOKEN, 'printer_id': print_id,
                'printer_info': new_info.encode('utf-8'), 'printer_status': new_status}
        encode_data = urllib.urlencode(data)
        url = PHP_PRINTERS_STATUS_URL + encode_data
        try:
            result = urllib.urlopen(url).read()
        except Exception, e:
            sqlite_log(
                event='send printer status', local_data=str(e), push_data=url)
        else:
            result_json = json.loads(result)
            sqlite_log(event='send printer status', local_data='function update_printer_status', push_data=url, response_status=result_json.get(
                'success'), response_data=result_json.get('result', None))


def get_url_data(app_id, app_secret, page_no):
    'get请求参数签名构造'
    status = 'WAIT_SELLER_SEND_GOODS'
    method = 'kdt.trades.sold.get'
    timestamp = TimeUtils.get_timestamp()
    v = '1.0'
    use_has_next = 'true'
    page_size = 500
    start_update = TimeUtils.get_start_created()
    sign = '%sapp_id%smethod%spage_no%dpage_size%dstart_update%sstatus%stimestamp%suse_has_next%sv%s%s' % (
        app_secret, app_id, method, page_no, page_size, start_update, status, timestamp, use_has_next, v, app_secret)
    md5_sign = hashlib.md5(sign).hexdigest()
    url_data = {'status': status, 'method': method, 'use_has_next': use_has_next,
                'timestamp': timestamp, 'v': v, 'sign': md5_sign, 'app_id': app_id,
                'page_no': page_no, 'page_size': page_size, 'start_update': start_update}
    data = urllib.urlencode(url_data)
    return data


def get_orders(user_id, app_id, app_secret, page_no):
    '''
    通过有赞API接口获得订单,正确的返回格式是:{"response":{"total_results":0,"trades":[]}}
    有订单的格式是:{"response": {"trades": [{"num": 1, "num_iid": "19575614", "price": "3.50", "pic_path": "http:\/\/imgqn.koudaitong.com\/upload_files\/2015\/04\/07\/FpDwHsHWMWRB_UhEJxFQgTBnP-Ch.jpg", "pic_thumb_path": "http:\/\/imgqn.koudaitong.com\/upload_files\/2015\/04\/07\/FpDwHsHWMWRB_UhEJxFQgTBnP-Ch.jpg!200x0.jpg", "title": "\u7edf\u4e00 \u6765\u4e00\u6876 \u8001\u575b\u9178\u83dc\u725b\u8089\u9762 \u6876\u88c5 \u6876\u9762 \u6ce1\u9762\u5373\u98df\u901f\u98df \u65b9\u4fbf\u9762", "type": "COD", "discount_fee": "0.00", "status": "WAIT_SELLER_SEND_GOODS", "shipping_type": "express", "post_fee": "0.00", "total_fee": "3.50", "refunded_fee": "0.00", "payment": "3.50", "created": "2015-05-12 21:06:57", "update_time": "2015-05-12 21:07:41", "pay_time": "2015-05-12 21:07:41", "pay_type": "CODPAY", "consign_time": "", "sign_time": "", "buyer_area": "\u5317\u4eac\u5e02\u5317\u4eac\u5e02", "seller_flag": 0, "buyer_message": "", "orders": [{"outer_sku_id": "", "outer_item_id": "", "title": "\u7edf\u4e00 \u6765\u4e00\u6876 \u8001\u575b\u9178\u83dc\u725b\u8089\u9762 \u6876\u88c5 \u6876\u9762 \u6ce1\u9762\u5373\u98df\u901f\u98df \u65b9\u4fbf\u9762",s                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               "seller_nick": "\u51e1\u5feb\u751f\u6d3b", "fenxiao_price": "0.00", "price": "3.50", "total_fee": "3.50", "payment": "3.50", "discount_fee": "0.00", "sku_id": 0, "sku_unique_code": "", "sku_properties_name": "", "pic_path": "http:\/\/imgqn.koudaitong.com\/upload_files\/2015\/04\/07\/FpDwHsHWMWRB_UhEJxFQgTBnP-Ch.jpg", "pic_thumb_path": "http:\/\/imgqn.koudaitong.com\/upload_files\/2015\/04\/07\/FpDwHsHWMWRB_UhEJxFQgTBnP-Ch.jpg!200x0.jpg", "item_type": 0, "buyer_messages": [], "order_promotion_details":[], "num_iid":"19575614", "num":"1"}], "fetch_detail":null, "coupon_details":[], "sub_trades":[], "weixin_user_id":"0", "buyer_nick":"", "tid":"E20150512210657921667948", "buyer_type":"0", "buyer_id":"0", "trade_memo":"", "receiver_city":"\u5317\u4eac\u5e02", "receiver_district":"\u671d\u9633\u533a", "receiver_name":"\u6731\u660e", "receiver_state":"\u5317\u4eac\u5e02", "receiver_address":"\u5316\u5de5\u5927\u5b661\u53f7\u697c116\u5bbf\u820d", "receiver_zip":"", "receiver_mobile":"18810463346", "feedback":0, "outer_tid":""}], "has_next": false}}
    如果有错误,格式是: {"error_response":{"code":40005,"msg":"invalid signature","params":{"status":"WAIT_SELLER_SEND_GOODS","timestamp":"2015-05-12 16:42:50","app_id":"6d3024789aa0b91bc3","sign":"256fcb4
    '''
    global TID_USERID_MC
    url_data = get_url_data(app_id, app_secret, page_no)
    try:
        orders_json_data = urllib.urlopen(YOUZAN_URL, url_data).read()
    except Exception, e:
        sqlite_log(event='get data from youzan', local_data=str(e))
    orders_data = json.loads(orders_json_data)
    if 'error_response' in orders_data:  # 如果返回错误
        sqlite_log(event='get orders from youzan', local_data='function get_orders:', response_data=orders_data['error_response']['msg'])
        # print TimeUtils.get_timestamp(), 'function get_orders,', orders_data['error_response']['msg']
    if 'response' in orders_data:  # 如果返回正确
        trades = orders_data['response']['trades']
        if trades:  # 如果有订单
            # print TimeUtils.get_timestamp(), 'trades.length: ', len(trades), 'page: ', page_no
            for trade in trades:
                # 将订单的tid和user_id发送给php处理
                # 如果mc里没有该tid
                if not TID_USERID_MC.get(trade['tid'].encode('utf-8')):
                    php_orders(user_id, trade)  # 发送给php接口
                    TID_USERID_MC.set(
                        trade['tid'].encode('utf-8'), user_id, MEMCACHE_TIME_OUT)
        if orders_data['response']['has_next']:  # 如果有下一页
            page = page_no + 1
            get_orders(user_id, app_id, app_secret, page)


def php_orders(user_id, trade):
    '将user_id和trade发送给php'
    data = {'token': TOKEN, 'params': json.dumps(trade), 'user_id': user_id}
    try:
        result = urllib2.urlopen(
            url=PHP_ORDER_URL, data=urllib.urlencode(data)).read()
    except Exception, e:
        sqlite_log(event='send orders', local_data=str(e), push_data=data)
    else:
        result_json = json.loads(result)
        sqlite_log(event='send orders', local_data='function php_orders', push_data=data, response_status=result_json.get(
            'success'), response_data=result_json.get('result', None))


def orders_job():
    userid_appid_secret = get_userid_appid_secret()
    if userid_appid_secret:
        for (user_id, app_id, app_secret) in userid_appid_secret:
            # 读取每个商家的订单,一个商家一个线程
            order_thread = OrderThread(user_id, app_id, app_secret)
            order_thread.start()
    else:  # 如果返回的是None(数据库连接出错)
        return


class TimeUtils():

    '一些获取格式化时间的工具方法'
    @staticmethod
    def get_timestamp():
        '返回格式化的时间戳'
        return time.strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def get_seconds():
        '获取当前时间的秒数'
        return datetime.datetime.now().second

    @staticmethod
    def get_start_created():
        '有赞接口开始交易时间,设置为5分钟之内的交易'
        some_time_ago = datetime.datetime.now(
        ) - datetime.timedelta(seconds=300)
        some_time_ago_format = some_time_ago.strftime('%Y-%m-%d %H:%M:%S')
        return some_time_ago_format


def get_userid_appid_secret():
    '获得所有商家的appid和appSecret'
    global DB_CONNECTION
    try:
        cur = DB_CONNECTION.cursor()
    except Exception, e:  # 如果数据库连接出错,就暂停5秒,重新连接,return None
        sqlite_log('db connect error', str(e))
        get_db_con()
    try:
        cur.execute(SQL_GET_APPID_SECRET)
    except:
        get_db_con()
        sqlite_log('db connect error', str(e))
        cur = DB_CONNECTION.cursor()
        cur.execute(SQL_GET_APPID_SECRET)
    rows = cur.fetchall()
    userid_appid_secret = []  # 存放(user_id, appid, secret)元组的列表
    for row in rows:
        if row[1] and row[2]:
            userid_appid_secret.append((row[0], row[1], row[2]))
    return userid_appid_secret


def get_db_con():
    '获得数据库连接'
    global DB_CONNECTION
    try:
        sqlite_log('db connecting', 'function get_db_con')
        DB_CONNECTION = MySQLdb.connect(
            host=DB_HOST, passwd=DB_PASSWORD, port=DB_PORT, user=DB_USER, db=DB_NAME, charset='utf8')
    except Exception, e:
        sqlite_log('db connect error', str(e))
        time.sleep(5)
        get_db_con()  # 重新连接


def get_new_printer_status(sn, key):
    '获得最新的打印机状态'
    params = {'sn': sn, 'key': key}
    encodedata = urllib.urlencode(params)
    urlstr = FEIE_HOST + FEIE_QUERY_PRINTER_STATUS_ACTION
    try:
        result = urllib2.urlopen(url=urlstr, data=encodedata).read()
    except urllib2.HTTPError, e:
        sqlite_log(event='get printer status error', local_data=str(
            e), push_data=urlstr + encodedata)
        return None
    else:
        result_data = json.loads(result)
        responseCode = result_data['responseCode']
        msg = result_data['msg']
        if responseCode == 1 and msg == u'请求参数错误':
            return ('0', u'参数错误')
        if responseCode == 0:
            if msg == u'离线':
                return ('0', u'离线')
            if msg == u'在线,纸张正常':
                return ('1', u'正常')
            if msg == u'在线,缺纸':
                return ('0', u'缺纸')


def get_feie_printer_status():
    '从数据库获取打印机信息'
    global DB_CONNECTION
    try:
        cur = DB_CONNECTION.cursor()
    except Exception, e:
        sqlite_log('get printer status form db', str(e))
        get_db_con()
        cur = DB_CONNECTION.cursor()
    try:
        cur.execute(SQL_GET_PRINT_STATUS)
    except Exception, e:
        sqlite_log('get printer status form db', str(e))
        get_db_con()
        cur = DB_CONNECTION.cursor()
        cur.execute(SQL_GET_PRINT_STATUS)
    rows = cur.fetchall()
    result = []
    for printer_id, number, key, status, info in rows:
        result.append((printer_id, number, key, status, info))
    return result


def print_status_job():
    printerid_number_key_status_info = get_feie_printer_status()  # 获取所有打印机
    if printerid_number_key_status_info:
        # 获取打印最新状态,和旧状态做比对,每个比对都是一个线程
        for printer_id, number, key, status, info in printerid_number_key_status_info:
            thread.start_new_thread(
                update_printer_status, (printer_id, number, key, status, info))


def sqlite_log(event, local_data, push_data=None, response_status=None, response_data=None):
    try:
        con = sqlite3.connect('log.db')
        cur = con.cursor()
        cur.execute('insert into log(event,local_data,push_data,response_status,response_data)values(%s,%s,%s,%s,%s)' % (
            event, local_data, push_data, response_status, response_data))
    except Exception, e:
        print TimeUtils.get_timestamp(), e
    con.commit()
    con.close()

if __name__ == '__main__':
    TID_USERID_MC = memcache.Client(['127.0.0.1:11211'])
    get_db_con()
    while 1:
        orders_job()  # 读取订单,判断选择新订单发给php
        print_status_job()  # 读取打印机状态,状态更新了就发给php
        if TimeUtils.get_seconds() == '10':  # 每分钟第10秒,断开数据库连接,重新连接
            DB_CONNECTION.close()
            get_db_con()
        time.sleep(1)
