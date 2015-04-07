# coding=utf-8
'''
Created on 2015年4月1日

@author: Administrator
'''

import urllib

result = urllib.urlopen('http://222.173.96.147/videos/v1/20140517/fd/ff/7c/0812388ff5b7dc2eaa1b07bbe21c2201.mp4?key=0505615e1abcccc8d19fa80a1b4413dac&src=iqiyi.com&m=v&qd_src=ih5&qd_tm=1427967258933&qd_ip=111.182.46.4&qd_sc=b309f104b09070549a769b2012bed61f&ip=111.182.46.4&uuid=a0a8310-551d0d1a-1a&qypid=2148583209_31').read()
f1 = open('swf.swf','wb')
f1.write(result)