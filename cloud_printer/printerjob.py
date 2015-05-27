# coding=utf-8
'''
Created on 2015年5月27日
监控打印机状态
@author: Administrator
'''
import time
import urllib
import urllib2
import json
import threading
import config
from config import TimeUtils


class UpdatePrinterStatusThread(threading.Thread):

    '更新打印机状态的线程'

    def __init__(self, print_id, number, key, status, info):
        threading.Thread.__init__(self)
        self.print_id = print_id
        self.number = number
        self.key = key
        self.status = status
        self.info = info

    def run(self):
        update_printer_status(
            self.print_id, self.number, self.key, self.status, self.info)


def update_printer_status(print_id, number, key, status, info):
    new_status, new_info = get_new_printer_status(number, key)
    if status != new_status or info != new_info:
        data = {'token': config.TOKEN, 'printer_id': print_id,
                'printer_info': new_info.encode('utf-8'), 'printer_status': new_status}
        encode_data = urllib.urlencode(data)
        url = config.PHP_PRINTERS_STATUS_URL + encode_data
        try:
            result = urllib.urlopen(url).read()
        except Exception, e:
            config.sqlite_log(
                event='send printer status', local_data=str(e), push_data=url)
        else:
            result_json = json.loads(result)
            config.sqlite_log(event='send printer status', local_data='function update_printer_status', push_data=url, response_status=result_json.get(
                'success'), response_data=result_json.get('result', None))


def get_new_printer_status(sn, key):
    '获得最新的打印机状态'
    params = {'sn': sn, 'key': key}
    encodedata = urllib.urlencode(params)
    urlstr = config.FEIE_HOST + config.FEIE_QUERY_PRINTER_STATUS_ACTION
    try:
        result = urllib2.urlopen(url=urlstr, data=encodedata).read()
    except urllib2.HTTPError, e:
        config.sqlite_log(event='get printer status error', local_data=str(
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
    '从redis获取打印机信息'
    r = config.get_redis_con()
    printer_ids = r.smembers('printers')
    printer_status = []
    for printer_id in printer_ids:
        printer = r.hgetall('printer:' + printer_id)
        if printer['printer_exp_time'] < TimeUtils.get_timestamp():
            printer_status.append((printer_id, printer['printer_key'], printer[
                                  'printer_status'], printer['printer_info']))
    return printer_status


def print_status_job():
    printerid_number_key_status_info = get_feie_printer_status()  # 获取所有打印机
    if printerid_number_key_status_info:
        # 获取打印最新状态,和旧状态做比对,每个比对都是一个线程
        printer_threads = []

        for printer_id, number, key, status, info in printerid_number_key_status_info:
            printer_thread = UpdatePrinterStatusThread(
                printer_id, number, key, status, info)
            printer_threads.append(printer_thread)

        for printer_thread in printer_threads:
            printer_thread.start()

        for printer_thread in printer_threads:
            printer_thread.join()

if __name__ == '__main__':
    while 1:
        print_status_job()  # 读取打印机状态,状态更新了就发给php
        time.sleep(1)
