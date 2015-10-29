# coding=utf-8
'''
Created on 2015年6月16日
联众平台验证码识别
@author: Administrator
'''
import MultipartPostHandler
import cookielib
import urllib2

user_name = 'xiaoqiu206'
user_pw = 'gfdsa308227746'
url = 'http://bbb4.hyslt.com/api.php?mod=php&act=upload'
yzm_minlen = '4'
yzm_maxlen = '4'
yzmtype_mark = 0
zztool_token = '6d7deaca0f3589a5744163e8aa3b4c4b'
params = {
    'user_pw': user_pw,
    'user_name': user_name,
    'yzm_minlen': yzm_minlen,
    'yzm_maxlen': yzm_maxlen,
    'yzmtype_mark': yzmtype_mark,
    # 'zztool_token': zztool_token,
    'upload': file('C:\CODE\yzm.jpg', 'rb')
}
cookies = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies), MultipartPostHandler.MultipartPostHandler)
res = opener.open(url, params)
print res.read()

'''
point_url = 'http://bbb4.hyslt.com/api.php?mod=php&act=point'
user_name = 'xiaoqiu206'
user_pw = 'gfdsa308227746'
params = {
    'user_name': user_name,
    'user_pw': user_pw
}
data = urllib.urlencode(params)
html = urllib2.urlopen(point_url,data)
print html.read()
'''
