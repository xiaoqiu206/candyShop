# coding=utf-8
'''
Created on 2015年7月1日
微盟打印机状态
@author: Administrator
'''
import gevent
from gevent import monkey
monkey.patch_all()

import urllib2
import json
import urllib
import time
import socket
socket.setdefaulttimeout(3)

import config


def get_printers():
    '从redis获取打印机状态和key'
    r = config.get_redis_con()
    printer_ids = r.smembers('weimob_printers')
    printers = []
    for printer_id in printer_ids:
        printer = r.hgetall('weimob_printer:' + printer_id)
    # print'old print:', printer['printer_status'], printer['printer_info'],
    # printer['printer_id']
        printers.append(printer)
#  print'get printers'
    return printers


def get_new_printer_info(printer):
    '获取最新的打印机状态并且比对'
#  print'get new printers'
    params = {'sn': printer['printer_number'], 'key': printer['printer_key']}
    encodedata = urllib.urlencode(params)
    urlstr = config.FEIE_HOST + config.FEIE_QUERY_PRINTER_STATUS_ACTION
    try:
        result = urllib2.urlopen(url=urlstr, data=encodedata, timeout=1).read()
    except Exception, e:
        config.sqlite_log(event='get wei meng print status', local_data=str(
            e), push_data=urlstr + encodedata)
    #  print'get new print error'
        return None
    else:
        #  print'get new info'
        result_data = json.loads(result)
    #  print'result_data:', result_data
        responseCode = result_data['responseCode']
        msg = result_data['msg']
        if responseCode == 1 and msg == u'请求参数错误':
            return ('0', u'参数错误')
        if responseCode == 0:
            if msg == u'离线':
                return ('0', msg)
            if msg == u'在线,纸张正常':
                return ('1', u'正常')
            if msg == u'在线,缺纸':
                return ('0', u'缺纸')


def compare(printer):
    '比较新旧状态'
    status_info = get_new_printer_info(printer)
#  print'new print:', status_info[0], status_info[1], printer['printer_id']
#  print'camparing'
    if status_info:
        if status_info[0].encode('utf-8') != printer['printer_status'] or status_info[1].encode('utf-8') != printer['printer_info']:
            printer['printer_status'] = status_info[0]
            printer['printer_info'] = status_info[1]
            g = gevent.spawn(push_to_php, printer)
            g.join()


def push_to_php(printer):
    data = {'token': config.WEIMOB_PRINTER_TOKEN, 'printer_id': printer['printer_id'].encode('utf-8'),
            'printer_info': printer['printer_info'].encode('utf-8'), 'printer_status': printer['printer_status'].encode('utf-8')
            }
    encode_data = urllib.urlencode(data)
    url = config.WEIMOB_PRINTER_URL + '&' + encode_data
    try:
        result = urllib.urlopen(url).read()
    #  print'push sucess'
    except Exception, e:
        config.sqlite_log(
            event='send weimeng printer status', local_data=str(e), push_data=url)
    else:
        result_json = json.loads(result)
        config.sqlite_log(event='send printer status', local_data='function update_printer_status', push_data=url, response_status=result_json.get(
            'success'), response_data=result_json.get('result', None))


def main():
    printers = get_printers()
    threads = []
    for printer in printers:
        thread = gevent.spawn(compare, printer)
        threads.append(thread)
    gevent.joinall(threads)


if __name__ == '__main__':
    while 1:
        main()
        time.sleep(1)
