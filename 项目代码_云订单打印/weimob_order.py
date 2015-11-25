# coding=utf-8
'''
Created on 2015年7月2日
微盟订单获取
@author: Administrator
'''
from gevent import monkey
monkey.patch_all()
import gevent

import time
import urllib
import json
import urllib2
import socket
socket.setdefaulttimeout(3)

import config


def get_accesstoken(user):
    m = config.get_memcache_con()
    return m.get('weimob_user:' + user['id']) or get_new_accesstoken(user)


def get_new_accesstoken(user):
    '重新生成accesstoken'
    url = config.WIEMOB_ACCESSTOKEN_GET_URL % (
        user['appid'], user['appsecret'])
    try:
        data = json.loads(urllib.urlopen(url).read())
    # printdata
    except Exception, e:
        config.sqlite_log(
            event='get new accesstoken', local_data=str(user), response_data=str(e))
    else:
        if data['code']['errcode'] == 0 and data['code']['errmsg'] == 'success':
            access_token = data['data']['access_token']
            m = config.get_memcache_con()
            m.set('weimob_user:' + user['id'], access_token, 7000)
            return access_token
        else:
            config.sqlite_log(
                event='get new accesstoken', local_data=str(user), response_data=data)


def get_users():
    '从redis获取user信息'
    r = config.get_redis_con()
    userids = r.smembers('weimob_users')
    users = []
    for userid in userids:
        user = r.hgetall('weimob_user:' + userid)
        user['id'] = userid
        users.append(user)
    return users


def get_orderlist(user, page_no=1):
    '返回订单列表'
    data = {
        'order_type': None,
        'order_source': None,
        # 'order_status': '1',
        'delivery_status': '0',
        'update_begin_time': config.TimeUtils.get_start_created(),
        'page_no': page_no,
        'page_size': 40
    }
    headers = {'Content-Type': 'application/json'}
    request = urllib2.Request(
        config.WEIMOB_ORDERLIST_GET_URL % user['accesstoken'], headers=headers, data=json.dumps(data))
    try:
        response = urllib2.urlopen(request)
    except Exception, e:
        config.sqlite_log(
            event='weimeng get orderlist', local_data=str(user), response_data=str(e))
        return None
    else:
        return response.read()


def get_order_id_nos(user):
    '获取order_id和order_no'
    page1 = 1
    order_id_nos = []
    m = config.get_memcache_con()

    while 1:
        orders = get_orderlist(user, page1)
        if not orders:
            return
        orders = json.loads(orders)
        # print orders
        if orders['code']['errcode'] == 0:  # 表示获取订单成功
            data = orders['data']
            page_count = data['page_count']  # 总页数
            page_no = data['page_no']  # 当前页码
            page_data = data['page_data']
            for each in page_data:
                # order_no是字符串,order_id是int
                order_no = each['order_no'].encode('utf-8')
                order_id = str(each['order_id'])
                if not m.get('weimob_orderno:' + order_no):
                    order_id_nos.append((order_id, order_no))
            page1 += 1
            if page_count <= page_no:
                break
    return order_id_nos


def handle_order_id_no(order_id_no, user):
    data = {'order_id': order_id_no[0], 'order_no': order_id_no[1]}
    headers = {'Content-Type': 'application/json'}

    request = urllib2.Request(
        config.WEIMOB_ORDER_GET % user['accesstoken'], headers=headers, data=json.dumps(data))
    try:
        result = urllib2.urlopen(request)
        result_data = result.read()
    except Exception, e:
        config.sqlite_log(
            event='weimeng get order', local_data=str(user), response_data=str(e))
        return
    json_data = json.loads(result_data)
    # print json_data['data'].get('order_no', 'no order')
    if json_data['code']['errcode'] == 0:
        g = gevent.spawn(php_order, user, json_data, order_id_no)
        g.join()


def php_order(user, json_data, order_id_no):
    data = json_data['data']
    php_data = {'token': config.WEIMOB_ORDER_PUSH_TOKEN, 'user_id': user['user_id'],
                'params': json.dumps(data)}

    # 如果是在线支付,未支付,就不发送给php,其他的(在线支付,已支付 和 线下支付)要发送给php
    if data['is_onlinepay'] and not data['pay_status']:
        return

    try:
        php_result = urllib2.urlopen(
            config.WEIMOB_ORDER_PUSH_URL, urllib.urlencode(php_data)).read()
        # print 'sending order to php', order_id_no
    except Exception, e:
        # print 'sending order failed', str(e)
        config.sqlite_log(
            event='send weimeng order to php', local_data=str(order_id_no), response_data=str(e))
    else:
        m = config.get_memcache_con()
        m.set('weimob_orderno:' +
              order_id_no[1], order_id_no[0], config.MEMCACHE_TIME_OUT)
        config.sqlite_log(event='send weimeng order to php sucess', local_data=str(
            order_id_no), response_data=php_result)


def handle_order(user):
    '处理订单的方法'
    # 获取accesstoken
    accesstoken = get_accesstoken(user)
    user['accesstoken'] = accesstoken
    # 获取订单号(列表)
    order_id_nos = get_order_id_nos(user)
    # 根据订单id和no,获取每个订单的详情并发送给php
    if order_id_nos:
        for order_id_no in order_id_nos:
            g = gevent.spawn(handle_order_id_no, order_id_no, user)
            g.join()


def main():
    users = get_users()
    gs = []
    for user in users:
        g = gevent.spawn(handle_order, user)
        gs.append(g)
    gevent.joinall(gs)


if __name__ == '__main__':
    while 1:
        main()
        time.sleep(1)
