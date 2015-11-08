# coding=utf-8
'''
Created on 2015年5月27日
监控新订单
@author: Administrator
'''
import time
import hashlib
import urllib
import urllib2
import json
import threading
import config
from config import TimeUtils


class OrderThread(threading.Thread):

    '处理商家订单'

    def __init__(self, user_id, app_id, app_secret, status):
        threading.Thread.__init__(self)
        self.user_id = user_id
        self.app_id = app_id
        self.app_secret = app_secret
        self.status = status

    def run(self):
        get_orders(
            self.user_id, self.app_id, self.app_secret, self.status, 1)


def get_url_data(app_id, app_secret, status, page_no):
    'get请求参数签名构造'
    # status = 'WAIT_SELLER_SEND_GOODS'
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


def get_orders(user_id, app_id, app_secret, status, page_no):
    '''
    通过有赞API接口获得订单,正确的返回格式是:{"response":{"total_results":0,"trades":[]}}
    有订单的格式是:{"response": {"trades": [{"num": 1, "num_iid": "19575614", "price": "3.50", "pic_path": "http:\/\/imgqn.koudaitong.com\/upload_files\/2015\/04\/07\/FpDwHsHWMWRB_UhEJxFQgTBnP-Ch.jpg", "pic_thumb_path": "http:\/\/imgqn.koudaitong.com\/upload_files\/2015\/04\/07\/FpDwHsHWMWRB_UhEJxFQgTBnP-Ch.jpg!200x0.jpg", "title": "\u7edf\u4e00 \u6765\u4e00\u6876 \u8001\u575b\u9178\u83dc\u725b\u8089\u9762 \u6876\u88c5 \u6876\u9762 \u6ce1\u9762\u5373\u98df\u901f\u98df \u65b9\u4fbf\u9762", "type": "COD", "discount_fee": "0.00", "status": "WAIT_SELLER_SEND_GOODS", "shipping_type": "express", "post_fee": "0.00", "total_fee": "3.50", "refunded_fee": "0.00", "payment": "3.50", "created": "2015-05-12 21:06:57", "update_time": "2015-05-12 21:07:41", "pay_time": "2015-05-12 21:07:41", "pay_type": "CODPAY", "consign_time": "", "sign_time": "", "buyer_area": "\u5317\u4eac\u5e02\u5317\u4eac\u5e02", "seller_flag": 0, "buyer_message": "", "orders": [{"outer_sku_id": "", "outer_item_id": "", "title": "\u7edf\u4e00 \u6765\u4e00\u6876 \u8001\u575b\u9178\u83dc\u725b\u8089\u9762 \u6876\u88c5 \u6876\u9762 \u6ce1\u9762\u5373\u98df\u901f\u98df \u65b9\u4fbf\u9762",s                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               "seller_nick": "\u51e1\u5feb\u751f\u6d3b", "fenxiao_price": "0.00", "price": "3.50", "total_fee": "3.50", "payment": "3.50", "discount_fee": "0.00", "sku_id": 0, "sku_unique_code": "", "sku_properties_name": "", "pic_path": "http:\/\/imgqn.koudaitong.com\/upload_files\/2015\/04\/07\/FpDwHsHWMWRB_UhEJxFQgTBnP-Ch.jpg", "pic_thumb_path": "http:\/\/imgqn.koudaitong.com\/upload_files\/2015\/04\/07\/FpDwHsHWMWRB_UhEJxFQgTBnP-Ch.jpg!200x0.jpg", "item_type": 0, "buyer_messages": [], "order_promotion_details":[], "num_iid":"19575614", "num":"1"}], "fetch_detail":null, "coupon_details":[], "sub_trades":[], "weixin_user_id":"0", "buyer_nick":"", "tid":"E20150512210657921667948", "buyer_type":"0", "buyer_id":"0", "trade_memo":"", "receiver_city":"\u5317\u4eac\u5e02", "receiver_district":"\u671d\u9633\u533a", "receiver_name":"\u6731\u660e", "receiver_state":"\u5317\u4eac\u5e02", "receiver_address":"\u5316\u5de5\u5927\u5b661\u53f7\u697c116\u5bbf\u820d", "receiver_zip":"", "receiver_mobile":"18810463346", "feedback":0, "outer_tid":""}], "has_next": false}}
    如果有错误,格式是: {"error_response":{"code":40005,"msg":"invalid signature","params":{"status":"WAIT_SELLER_SEND_GOODS","timestamp":"2015-05-12 16:42:50","app_id":"6d3024789aa0b91bc3","sign":"256fcb4
    '''
    args = locals()
    url_data = get_url_data(app_id, app_secret, status, page_no)
    try:
        orders_json_data = urllib.urlopen(config.YOUZAN_URL, url_data).read()
    except Exception, e:
        config.sqlite_log(event='get data from youzan', local_data=str(e))
        return
    try:
        if user_id in ('98', '99'):
            config.sqlite_log(event='order info', local_data=str(
                args),  response_data=orders_json_data)
        orders_data = json.loads(orders_json_data)
    except Exception, e:
        config.sqlite_log('function get_orders',
                          'orders_data = json.loads(orders_json_data)', None, orders_json_data, str(e))
    else:
        if 'error_response' in orders_data:  # 如果返回错误

            config.sqlite_log(event='get orders from youzan', push_data=url_data, local_data=str(args),
                              response_data=orders_data)
        if 'response' in orders_data:  # 如果返回正确
            trades = orders_data['response']['trades']
            if trades:  # 如果有订单,将订单的tid和user_id发送给php处理
                for trade in trades:
                    # 如果mc里没有该tid
                    if not config.get_memcache_con().get(trade['tid'].encode('utf-8')):
                        php_orders(user_id, trade)  # 发送给php接口
                        config.get_memcache_con().set(
                            trade['tid'].encode('utf-8'), user_id, config.MEMCACHE_TIME_OUT)
            if orders_data['response']['has_next']:  # 如果有下一页
                page = page_no + 1
                get_orders(user_id, app_id, app_secret, status, page)


def php_orders(user_id, trade):
    '将user_id和trade发送给php'
    data = {'token': config.TOKEN,
            'params': json.dumps(trade), 'user_id': user_id}
    try:
        result = urllib2.urlopen(
            url=config.PHP_ORDER_URL, data=urllib.urlencode(data)).read()
    except Exception, e:
        config.sqlite_log(
            event='send orders', local_data=str(e), push_data=data)
    else:
        try:
            result_json = json.loads(result)
            config.sqlite_log(event='send orders', local_data='function php_orders', push_data=data, response_status=result_json.get(
                'success'), response_data=result_json.get('result', None))
        except Exception, e:
            config.sqlite_log(
                'send orders', 'function php_orders', data, None, None)


def orders_job():
    '主方法,获取商家key等信息,得到最近的需要打印,发货的订单,发送到php接口'
    userid_appid_secret_hasvirtual = get_userid_appid_secret_hasvirtual()
    if userid_appid_secret_hasvirtual:
        threads = []
        for (user_id, app_id, app_secret, hasvirtual) in userid_appid_secret_hasvirtual:
            '''
            WAIT_SELLER_SEND_GOODS（等待卖家发货，即：买家已付款）
            WAIT_BUYER_CONFIRM_GOODS（等待买家确认收货，即：卖家已发货）
            '''
            order_thread = OrderThread(
                user_id, app_id, app_secret, 'WAIT_SELLER_SEND_GOODS')
            threads.append(order_thread)
            # 虚拟商品下单后就是默认已经发货了,所以如果商家有卖虚拟商品,还要获取已经付款的订单
            if hasvirtual == '1':
                order_thread1 = OrderThread(
                    user_id, app_id, app_secret, 'WAIT_BUYER_CONFIRM_GOODS')
                threads.append(order_thread1)
        for order_thread in threads:
            order_thread.start()
        for order_thread in threads:
            order_thread.join()


def get_userid_appid_secret_hasvirtual():
    '获得所有商家的appid和appSecret'
    r = config.get_redis_con()
    user_ids = r.smembers('users')
    userid_appid_secret_hasvirtual = []  # 存放(user_id, appid, secret)元组的列表
    for userid in user_ids:
        user = r.hgetall('user:' + userid)
        appid = user.get('appid', '')
        appsecret = user.get('appsecert', '')
        hasvirtual = user.get('virtual', '')
        userid_appid_secret_hasvirtual.append(
            (userid, appid, appsecret, hasvirtual))
    return userid_appid_secret_hasvirtual


if __name__ == '__main__':
    while 1:
        orders_job()  # 读取订单,判断选择新订单发给php
        time.sleep(1)
