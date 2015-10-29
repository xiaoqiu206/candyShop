# coding=utf-8
'''
Created on 2015年6月19日
代码清单1-1 基础:hello.py
@author: Administrator
'''
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web


# 从命令行中读取设置
'''
命令行输入python hello.py --help 时会出现2条帮助,
C:\workspace\Python_project2\tornadodemo>python hello.py --help
Usage: hello.py [OPTIONS]

Options:

  --help                           show this help information
  --port                           run on the given port (default 8000)
tornado使用type参数进行基本的参数类型验证,当不适合的类型被给出时,会抛出异常  
因此,允许一个整数的port参数作为options.port来访问程序,如果用户没有指定值,
则默认为8000
'''
from tornado.options import define, options
define('port', default=8000, help='run on the given port', type=int)


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        ''' 
        从一个查询字符串中取得参数greetion的值,如果这个参数没有出现在
        查询字符串中,tornado将使用get_argument的第二个参数作为默认值.
        '''
        greeting = self.get_argument('greeting', 'Hello')
        self.write(greeting + ', friendly user!')

if __name__ == '__main__':
    # 使用tornado额options模块来解析命令行
    tornado.options.parse_command_line() 
    # 创建一个tornado的application类的实例
    app = tornado.web.Application(handlers=[(r'/', IndexHandler)])
    ''' 从这里开始的代码将会被反复使用,一旦application对象被创建,我们可以
    将其传递给tornado的httpserver对象,然后使用我们再命令行指定的端口进行监听(通过options对象取出)
    最后,再程序准备好接受HTTP请求后,我们创建一个tornado的IOLoop的实例
    '''
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
