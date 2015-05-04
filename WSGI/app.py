# coding=utf-8
'''
Created on 2015年5月4日

@author: Administrator
'''
def application(environ, start_response):
    method = environ['REQUEST_METHOD']
    path = environ['PATH_INFO']
    if method == 'GET':
        return handle_home(environ, start_response)
    if method == 'POST' and path == '/signin':
        return handle_signin(environ, start_response)


def handle_home(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return '<h1>hello world! %s</h1>' % environ['PATH_INFO']


def handle_signin(environ, start_response):
    start_response('200 OK')
    return u'<h1>%s登录</h1>' % environ['PATH_INFO']