'''
Created on 2015年7月5日
发送邮件
@author: Administrator
'''
import smtplib
from email.mime.text import MIMEText
from email.header import Header

sender = "308227746@qq.com"
receiver = "xiaoqiu206@163.com"
subject = "测试邮件"
smtpserver = "smtp.qq.com"
username = sender
password = 'gfdsa308227746'

msg = MIMEText('测试内容,无需回复', 'plain', 'utf-8')
msg['Subject'] = Header(subject, 'utf-8')

smtp = smtplib.SMTP()
smtp.connect(smtpserver)
smtp.login(username, password)
smtp.sendmail(sender, receiver, msg.as_string())
smtp.quit()
