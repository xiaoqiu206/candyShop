# coding=utf-8
'''
Created on 2015年6月16日
用pycurl上传文件
@author: Administrator
'''
import pycurl
import os
import StringIO

buf = StringIO.StringIO()
user_name = 'xiaoqiu206'
user_pw = 'gfdsa308227746'
url = 'http://bbb4.hyslt.com/api.php?mod=php&act=upload'
yzm_minlen = '4'
yzm_maxlen = '4'
yzmtype_mark = '0'
zztool_token = '6d7deaca0f3589a5744163e8aa3b4c4b'

pc = pycurl.Curl()
pc.setopt(pycurl.WRITEFUNCTION,buf.write)
pc.setopt(pycurl.POST, 1)
pc.setopt(pycurl.URL, 'http://bbb4.hyslt.com/api.php?mod=php&act=upload')
pc.setopt(pycurl.HTTPPOST, [
    ('upload', (pc.FORM_FILE, os.path.join(
     os.path.dirname(os.path.abspath(__file__)), 'genimg.jpg'))),
    ('user_name', (pc.FORM_CONTENTS, user_name)),
    ('user_pw', (pc.FORM_CONTENTS, user_pw)),
    ('yzm_minlen', (pc.FORM_CONTENTS, yzm_minlen)),
    ('yzm_maxlen', (pc.FORM_CONTENTS, yzm_maxlen)),
    ('yzmtype_mark', (pc.FORM_CONTENTS, yzmtype_mark))

])

pc.perform()
print buf.getvalue()
pc.close()
