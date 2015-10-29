# coding=utf-8
'''
Created on 2015年10月15日
__foo__:一种约定,python内部的名字,用来区别其他用户自定义的命名,以防冲突.
_foo:一种约定,用来指定变量私有.程序员用来指定私有变量的一种方式.
__foo:这个有真正的意义,解析器用_classname__foo来代替这个名字,以区别和其他类相同的命名.
详情见http://www.zhihu.com/question/19754941
@author: xiaoq
'''


class MyClass():

    def __init__(self):
        self.__superprivate = 'hello'
        self._semiprivate = 'world'

mc = MyClass()
print mc.__dict__
print mc._MyClass__superprivate
print mc._semiprivate
print mc.__superprivate  # 异常