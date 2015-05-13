# coding=utf-8
'''
Created on 2015年5月12日
云打印,自动获取订单
@author: Administrator
'''
import MySQLdb
import time
import hashlib
import urllib
import json


# php接口
TOKEN = 'jj24l5na090h2kq309ah2'  # 接口token值
PHP_ORDER_URL = 'http://localhost/python_api'  # php处理订单的API的url

# 阿里云数据库连接参数
DB_HOST = 'tangmi2015.mysql.rds.aliyuncs.com'
DB_PORT = 3306
DB_USER = 'printergiahoocom'
DB_PASSWORD = '231f5407'
DB_NAME = 'printergiahoocom'

# SQL语句模板
# 获取user_id,app_id,app_secret
SQL_GET_APPID_SECRET = 'SELECT user_id, user_appid, user_appsecert FROM printer_user'


# 调用有赞API(查询卖家已卖出的交易列表)调用参数
YOUZAN_URL = 'http://open.koudaitong.com/api/entry'


def get_url_data(app_id, app_secret, page_no):
    'get请求参数签名构造'
    status = 'WAIT_SELLER_SEND_GOODS'
    method = 'kdt.trades.sold.get'
    timestamp = get_timestamp()
    v = '1.0'
    use_has_next = 'true'
    sign = '%sapp_id%smethod%spage_no%dstatus%stimestamp%suse_has_next%sv%s%s' % (
        app_secret, app_id, method, page_no, status, timestamp, use_has_next, v, app_secret)
    md5_sign = hashlib.md5(sign).hexdigest()
    url_data = {'status': status, 'method': method, 'use_has_next': use_has_next,
                'timestamp': timestamp, 'v': v, 'sign': md5_sign, 'app_id': app_id, 'page_no':page_no}
    data = urllib.urlencode(url_data)
    print 'urldata: ', data
    return data


def get_orders(user_id, app_id, app_secret, page_no):
    '''
    通过有赞API接口获得订单,正确的返回格式是:{"response":{"total_results":0,"trades":[]}}
    有订单的格式是:{"response": {"trades": [{"num": 1, "num_iid": "19575614", "price": "3.50", "pic_path": "http:\/\/imgqn.koudaitong.com\/upload_files\/2015\/04\/07\/FpDwHsHWMWRB_UhEJxFQgTBnP-Ch.jpg", "pic_thumb_path": "http:\/\/imgqn.koudaitong.com\/upload_files\/2015\/04\/07\/FpDwHsHWMWRB_UhEJxFQgTBnP-Ch.jpg!200x0.jpg", "title": "\u7edf\u4e00 \u6765\u4e00\u6876 \u8001\u575b\u9178\u83dc\u725b\u8089\u9762 \u6876\u88c5 \u6876\u9762 \u6ce1\u9762\u5373\u98df\u901f\u98df \u65b9\u4fbf\u9762", "type": "COD", "discount_fee": "0.00", "status": "WAIT_SELLER_SEND_GOODS", "shipping_type": "express", "post_fee": "0.00", "total_fee": "3.50", "refunded_fee": "0.00", "payment": "3.50", "created": "2015-05-12 21:06:57", "update_time": "2015-05-12 21:07:41", "pay_time": "2015-05-12 21:07:41", "pay_type": "CODPAY", "consign_time": "", "sign_time": "", "buyer_area": "\u5317\u4eac\u5e02\u5317\u4eac\u5e02", "seller_flag": 0, "buyer_message": "", "orders": [{"outer_sku_id": "", "outer_item_id": "", "title": "\u7edf\u4e00 \u6765\u4e00\u6876 \u8001\u575b\u9178\u83dc\u725b\u8089\u9762 \u6876\u88c5 \u6876\u9762 \u6ce1\u9762\u5373\u98df\u901f\u98df \u65b9\u4fbf\u9762",s                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               "seller_nick": "\u51e1\u5feb\u751f\u6d3b", "fenxiao_price": "0.00", "price": "3.50", "total_fee": "3.50", "payment": "3.50", "discount_fee": "0.00", "sku_id": 0, "sku_unique_code": "", "sku_properties_name": "", "pic_path": "http:\/\/imgqn.koudaitong.com\/upload_files\/2015\/04\/07\/FpDwHsHWMWRB_UhEJxFQgTBnP-Ch.jpg", "pic_thumb_path": "http:\/\/imgqn.koudaitong.com\/upload_files\/2015\/04\/07\/FpDwHsHWMWRB_UhEJxFQgTBnP-Ch.jpg!200x0.jpg", "item_type": 0, "buyer_messages": [], "order_promotion_details":[], "num_iid":"19575614", "num":"1"}], "fetch_detail":null, "coupon_details":[], "sub_trades":[], "weixin_user_id":"0", "buyer_nick":"", "tid":"E20150512210657921667948", "buyer_type":"0", "buyer_id":"0", "trade_memo":"", "receiver_city":"\u5317\u4eac\u5e02", "receiver_district":"\u671d\u9633\u533a", "receiver_name":"\u6731\u660e", "receiver_state":"\u5317\u4eac\u5e02", "receiver_address":"\u5316\u5de5\u5927\u5b661\u53f7\u697c116\u5bbf\u820d", "receiver_zip":"", "receiver_mobile":"18810463346", "feedback":0, "outer_tid":""}], "has_next": false}}
    如果有错误,格式是: {"error_response":{"code":40005,"msg":"invalid signature","params":{"status":"WAIT_SELLER_SEND_GOODS","timestamp":"2015-05-12 16:42:50","app_id":"6d3024789aa0b91bc3","sign":"256fcb4
    '''
    url_data = get_url_data(app_id, app_secret, page_no)
    orders_json_data = urllib.urlopen(YOUZAN_URL, url_data).read()
    orders_data = json.loads(orders_json_data)
    if 'error_response' in orders_data:  # 如果返回错误
        print orders_data['error_response']['msg']
        pass  # 记录日志
    if 'response' in orders_data:  # 如果返回正确
        trades = orders_data['response']['trades']
        if trades:  # 如果有订单
            print u'trades.length: ', len(trades), 'page: ', page_no
            for trade in trades:
                print user_id, trade['tid']
                # php_orders(user_id, trade['tid'])  # 将订单的tid和user_id发送给php
        if orders_data['response']['has_next']:  # 如果有下一页
            page = page_no + 1
            get_orders(user_id, app_id, app_secret, page)


def php_orders(user_id, tid):
    '将user_id和tid发送给php'
    data = {'token': TOKEN, 'tid': tid, 'user_id': user_id}
    url_data = urllib.urlencode(data)
    urllib.urlopen(PHP_ORDER_URL, url_data)


def orders_job():
    userid_appid_secret = get_userid_appid_secret()
    for (user_id, app_id, app_secret) in userid_appid_secret:
        get_orders(user_id, app_id, app_secret, 1)


def get_timestamp():
    '返回格式化的时间戳'
    return time.strftime('%Y-%m-%d %H:%M:%S')


def get_userid_appid_secret():
    '获得所有商家的appid和appSecret'
    con = MySQLdb.connect(
        host=DB_HOST, passwd=DB_PASSWORD, port=DB_PORT, user=DB_USER, db=DB_NAME)
    cur = con.cursor()
    cur.execute(SQL_GET_APPID_SECRET)
    rows = cur.fetchall()
    userid_appid_secret = []  # 存放(user_id, appid, secret)元组的列表
    for row in rows:
        if row[1] and row[2]:
            userid_appid_secret.append((row[0], row[1], row[2]))
    return userid_appid_secret


if __name__ == '__main__':
    while 1:
        orders_job()
        time.sleep(40)