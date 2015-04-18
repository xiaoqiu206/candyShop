# coding=utf-8
'''
Created on 2015年4月18日
ftp和ssh批量验证
@author: Administrator
'''
import threading 
from time import sleep, ctime
from ftplib import FTP
import paramiko
from paramiko.client import AutoAddPolicy


class MyThread(threading.Thread):
    def __init__(self, url, protocol, username, password):
        threading.Thread.__init__(self)
        self.url = url
        self.protocol = protocol
        self.username = username
        self.password = password
        
    def run(self):
        validate(self.url, self.protocol, self.username, self.password)
    

def validate(url, protocol, username, password):
    if protocol == 'ftp':
        try:
            ftp = FTP(url)
        except:
            print url, u'没有开放21端口'
            return 
        try:
            ftp.login(username, password)
        except:
            print ctime(), url, protocol, username, password, u'用户名密码错误'
            return
        print ctime(), url, protocol, username, password, u'登陆成功'
    else:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(url, 22, username, password)
        except:
            print ctime(), url, protocol, username, password, u'无法登陆'
            return
        print ctime(), url, protocol, username, password, u'登陆成功','\n'
        
        
def many():
    f1 = open('text.txt')
    for line in f1:
        vks = line.split(' ')
        my_thread = MyThread(vks[0], vks[1], vks[2], vks[3].replace('\n', ''))
        my_thread.run()

        
if __name__ == '__main__':
    many()
