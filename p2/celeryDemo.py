# coding=utf-8
'''
Created on 2015年7月24日
celery的demo
@author: Administrator
'''
import time
from celery import Celery

celery = Celery('task', broker='redis://localhost:6379/0')


@celery.task
def sendmail(mail):
    print 'sending mail to %s' % mail['to']
    time.sleep(2.0)
    print 'mail sent'

