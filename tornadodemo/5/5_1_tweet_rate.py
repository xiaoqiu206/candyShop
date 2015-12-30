# coding=utf-8
'''
Created on 2015年6月26日
同步http请求
@author: Administrator
'''
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from uuid import uuid4


class DetailHandler(tornado.web.RequestHandler):
    "用来渲染HTML"

    def get(self):
        """
                  为每个页面请求产生一个唯一标识符,在每次请求时提供库存数量,
                  并向浏览器渲染index.html模版
        """
        session = uuid4()
        count = self.application.shoppingCart.getInventoryCount()
        self.render('index.html', session=session, count=count)


class CartHandler(tornado.web.RequestHandler):
    "提供操作购物车的接口"

    def post(self):
        """
                    提供API来请求从访客的购物车中添加和删除物品
        """
        action = self.get_argument('action')
        session = self.get_argument('session')

        if not session:
            self.set_status(400)
            return

        if action == 'add':
            self.application.shoppingCart.moveItemToCart(session)
        elif action == 'remove':
            self.application.shoppingCart.removeItemFromCart(session)
        else:
            self.set_status(400)


class StatusHandler(tornado.web.RequestHandler):
    "查询全局库存变化的通知"
    @tornado.web.asynchronous
    def get(self):
        """
                注册了一个带有购物车控制器的回调函数
        用self.asycn_callback包住回调函数以确保回调函数中引发的异常不会使RequestHandler关闭连接
        """
        self.application.shoppingCart.register(
            self.async_callback(self.on_message()))

    def on_message(self, count):
        self.write('{"inventoryCount": "%d"}' % count)


class ShoppingCart(object):
    totolInventory = 10  # 总存货
    callbacks = []
    carts = {}

    def register(self, callback):
        self.callbackss.append(callback)

    def moveItemToCart(self, session):
        if session in self.carts:
            return

        self.carts[session] = True
        self.notifyCallbacks()

    def removeItemFromCart(self, session):
        if session not in self.carts:
            return

        del(self.carts[session])
        self.notifyCallbacks()

    def notifyCallbacks(self):
        for c in self.callbacks:
            self.callbackHelper(c)

        self.callbacks = []

    def callbackHelper(self, callback):
        callback(self.getInventoryCount())

    def getInventoryCount(self):
        return self.totolInventory - len(self.carts)


class Application(tornado.web.Application):

    def __init__(self):
        self.shoppingCart = ShoppingCart()

        handlers = [
            (r'/', DetailHandler),
            (r'/cart', CartHandler),
            (r'/cart/status', StatusHandler)
        ]

        settings = {
            'template_path': 'templates',
            'static_path': 'static'
        }

        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    tornado.options.parse_command_line()

    app = Application()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
