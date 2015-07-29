# coding=utf-8
'''
Created on 2015年7月22日

@author: Administrator
'''



data = {'password': password, 'sei': sei, 'mei': mei,
        'sei_kana': sei_kana, 'mei_kana': mei_kana, 'tel1': tel1,
        'tel2': tel2, 'tel3': tel3, 'sbmt': '次へ'
        }
request5 = urllib2.Request(
    NAME_PWD_TEL_URL, data=urllib.urlencode(data), headers=headers)