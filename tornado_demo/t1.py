# coding=utf-8
'''
Created on 2016年4月9日
tornado websocket的练习1
@author: xiaoq
'''
import tornado.ioloop
import tornado.options
import tornado.websocket

import logging
import os.path

from tornado.options import define, options

define('port', default=80, help='run on the given port')
define('host', default='0.0.0.0', help="run on the given host")


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/chatsocket', ChatSocketHandler),
            (r'/test', TestSocketHandler),
        ]
        settings = dict(
            cookie_secret="lsadjfolasjfd",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("index.html")


class TestSocketHandler(tornado.websocket.WebSocketHandler):

    clients = set()

    def open(self):
        TestSocketHandler.clients.add(self)
        logging.info("%s websocket connect" % self.request.remote_ip)

    def on_close(self):
        logging.info("%s websocket close" % self.request.remote_ip)
        TestSocketHandler.clients.remove(self)
        
    def on_message(self, message):
        logging.info("%s get message %s" % (self.request.remote_ip,message))
        self.send_to_all(message)

    def send_to_all(self,message):
        for c in TestSocketHandler.clients:
            if c is not self:
                c.write_message(message)


class ChatSocketHandler(tornado.websocket.WebSocketHandler):
    pass


def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
