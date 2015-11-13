# coding=utf-8
'''
Created on 2015年5月27日
监控新订单
@author: Administrator
'''
from gevent import monkey
monkey.patch_all()
import gevent
import time
import hashlib
import urllib
import urllib2
import json
import config
from config import TimeUtils
import socket
socket.setdefaulttimeout(5)


def create_url(user, status, page_no):
    app_id = user.get('appid')
    app_secret = user.get('appsecret') or user.get('appsecert')
    access_token = user.get('accesstoken')

    # 请求参数构造
    method = 'kdt.trades.sold.get'
    timestamp = TimeUtils.get_timestamp()
    v = '1.0'
    use_has_next = 'true'
    page_size = 100
    start_update = TimeUtils.get_start_created()

    if app_id and app_secret:

        sign = '%sapp_id%smethod%spage_no%dpage_size%dstart_update%sstatus%stimestamp%suse_has_next%sv%s%s' % (
            app_secret, app_id, method, page_no, page_size, start_update, status, timestamp, use_has_next, v, app_secret)
        md5_sign = hashlib.md5(sign).hexdigest()
        url_data = {'status': status, 'method': method, 'use_has_next': use_has_next,
                    'timestamp': timestamp, 'v': v, 'sign': md5_sign, 'app_id': app_id,
                    'page_no': page_no, 'page_size': page_size, 'start_update': start_update}
        url = config.YOUZAN_URL_APPID_SECRET + urllib.urlencode(url_data)

    if access_token:
        url_data = {'status': status, 'method': method, 'use_has_next': use_has_next,
                    'timestamp': timestamp, 'v': v, 'access_token': access_token,
                    'page_no': page_no, 'page_size': page_size, 'start_update': start_update}
        url = config.YOUZAN_URL_ACCESSTOKEN + urllib.urlencode(url_data)
    return url


def get_token(user):
    data = {'grant_type': 'refresh_token', 'refresh_token': user.get(
        'refresh_token'), 'client_id': user.get('client_id'), 'client_secret': user.get('client_secret')}
    req = urllib2.Request(
        config.YOUZAN_URL_REFRESH_TOKEN, urllib.urlencode(data))
    response = urllib2.urlopen(req)
    the_page = response.read()
    return the_page


def get_orders(user, status, page_no):
    url = create_url(user, status, page_no)
    try:
        orders_json_data = urllib.urlopen(url).read()
    except Exception, e:
        config.sqlite_log(event='get data from youzan', local_data=str(user))
        return
    try:
        config.mysql_log(event='order info', local_data=user[
                         'user_id'], push_data=url,  response_data=orders_json_data)
        orders_data = json.loads(orders_json_data)
    except Exception, e:
        config.sqlite_log('function get_orders',
                          'orders_data = json.loads(orders_json_data)', None, orders_json_data, str(e))
    else:
        # 如果accesstoken失效,重新获取
        error_response = orders_data.get('error_response')
        if error_response and error_response['code'] in (40010, 40011):
            get_token(user)

        if 'response' in orders_data:  # 如果返回正确
            trades = orders_data['response']['trades']
            if trades:  # 如果有订单,将订单的tid和user_id发送给php处理
                for trade in trades:
                        # 如果mc里没有该tid
                    if not config.get_memcache_con().get(trade['tid'].encode('utf-8')):
                        php_orders(user['user_id'], trade)  # 发送给php接口
                        config.get_memcache_con().set(
                            trade['tid'].encode('utf-8'), user['user_id'], config.MEMCACHE_TIME_OUT)
            if orders_data['response']['has_next']:  # 如果有下一页
                page = page_no + 1
                get_orders(user, status, page)


def get_url_data(app_id, app_secret, status, page_no):
    'get请求参数签名构造'
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
    users = get_users()
    if users:
        gs = []
        for user in users:
            '''
            WAIT_SELLER_SEND_GOODS（等待卖家发货，即：买家已付款）
            WAIT_BUYER_CONFIRM_GOODS（等待买家确认收货，即：卖家已发货）
            '''
            g = gevent.spawn(
                get_orders, user, 'WAIT_SELLER_SEND_GOODS', 1)

            gs.append(g)
            # 虚拟商品下单后就是默认已经发货了,所以如果商家有卖虚拟商品,还要获取已经付款的订单
            if user.get('virtual') == '1':
                g1 = gevent.spawn(
                    get_orders, user, 'WAIT_BUYER_CONFIRM_GOODS', 1)
                gs.append(g1)
            gevent.joinall(gs)


def get_users():
    '获得所有商家的appid和appSecret'
    r = config.get_redis_con()
    user_ids = r.smembers('users')
    users = []
    for userid in user_ids:
        user = r.hgetall('user:' + userid)
        user['user_id'] = userid
        users.append(user)
    return users


def main():
    while 1:
        orders_job()
        time.sleep(1)

if __name__ == '__main__':
    main()
