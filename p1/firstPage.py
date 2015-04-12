# coding=utf-8
'''
Created on 2015年3月31日
第一页的数据
@author: Administrator
'''
from bs4 import BeautifulSoup as BS
import urllib2


opener = urllib2.build_opener()
headers = {
            'Accept-Encoding':"gzip, deflate",
            'Connection': 'keep-alive',
            'Host': 'cs.500.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0',
            'Accept': 'image/png,image/*;q=0.8,*/*;q=0.5',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Referer': 'http://odds.500.com/fenxi/ouzhi-452241.shtml?ctype=2',
            'Cookie': 'WT_FPC=id=undefined:lv=1428745247545:ss=1428743431036; Hm_lvt_4f816d475bb0b9ed640ae412d6b42cab=1427853826,1427878001,1428743431; bdshare_firstime=1427853826255; CLICKSTRN_ID=27.25.40.46-1427853828.439439::B9E4BB62AB0A6CF3860ACB4AFAA790F5; __utma=63332592.1563532881.1427853827.1427878002.1428743432.3; __utmz=63332592.1427853827.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ck_RegFromUrl=http%3A//odds.500.com/fenxi/ouzhi-452241.shtml%3Fctype%3D2; sdc_session=1428743431038; sdc_userflag=1428743431038::1428745247546::7; Hm_lpvt_4f816d475bb0b9ed640ae412d6b42cab=1428745247; __utmb=63332592.7.10.1428743432; __utmc=63332592; motion_id=1428744770307_0.4782532854401409; ck_RegUrl=odds.500.com'
           }
request = urllib2.Request('http://odds.500.com/fenxi/ouzhi-452241.shtml?ctype=2', headers=headers)
html = opener.open(request)








