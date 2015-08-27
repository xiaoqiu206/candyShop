# coding=utf-8
'''
Created on 2015年8月2日

@author: Administrator
'''
from tornado.web import RequestHandler, Application, asynchronous
from tornado.web import Application
from tornado.ioloop import IOLoop


class MainHandler(RequestHandler):

    @asynchronous
    def get(self):
        self.write('hello world')
        self.finish()

application = Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    IOLoop.instance().start()
