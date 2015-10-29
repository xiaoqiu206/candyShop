#coding=utf-8
'''
Created on 2015年6月26日
同步http请求
@author: Administrator
'''
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import urllib
import datetime
import time

from tornado.options import define, options
define('port', default=8000, help='run')
