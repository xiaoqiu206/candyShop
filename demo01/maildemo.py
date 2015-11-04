# coding=utf-8
'''
Created on 2015年7月17日
收取邮件
@author: Administrator
'''
'''
from poplib import POP3
import time


while 1:
    p = POP3('pop.mail.yahoo.co.jp')
    p.user('tennis_295558348@yahoo.co.jp')
    p.pass_('july8866')
    email_num = p.stat()
    p.quit()
    print email_num

time.sleep(1)
'''

import urllib2
import time

t1 = time.time()
url = 'http://aksale.advs.jp/cp/akachan_sale_pc/_mail.cgi?sbmt=%97%5C%96%F1&event_id=0960482165&event_type=5'
headers = {
    'Host': 'aksale.advs.jp',
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0"
}
request = urllib2.Request(url, headers=headers)
html = urllib2.urlopen(request).read()
print html
print time.time() - t1