# coding=utf-8
'''
Created on 2015年10月16日
装饰器是一个很著名的设计模式，经常被用于有切面需求的场景，较为经典的有插入日志、性能测试、事务处理等。
装饰器是解决这类问题的绝佳设计，有了装饰器，我们就可以抽离出大量函数中与函数功能本身无关的雷同代码并继续重用。
概括的讲，装饰器的作用就是为已经存在的对象添加额外的功能。
推荐 http://taizilongxu.gitbooks.io/stackoverflow-about-python/content/3/README.html
@author: xiaoq
'''
# 先看看简单的一个函数有2个装饰器

# 字体变粗装饰器


def makebold(fn):
    # 装饰器将返回新的函数
    def wrapper():
        return '<b>' + fn() + '</bn>'
    return wrapper

# 斜体装饰器


def makeitalic(fn):
    # 装饰器将返回新的函数
    def wrapper():
        # 在之前或之后插入新的代码
        return '<i>' + fn() + '</i>'
    return wrapper


@makebold
@makeitalic
def say():
    return 'hello'

print say()
'''
结果是 <b><i>hello</b></i>
这相当于
def say():
    return 'hello' 
say = makeblod(makeitalic(say))
print say()
'''




