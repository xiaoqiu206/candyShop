#coding=utf-8
'''
Created on 2015年10月9日
python其实有3个方法:静态方法,类方法和实例方法
这里先理解下函数参数里面的self和cls,self和cls是对类或者实例的绑定,对于一般的函数我们可以这么调用foo(x)
这个函数是最常用的,它的工作跟任何东西(类,实例)无关.对于实例方法,我们知道在类里每次定义方法的时候都需要绑定这个实例,
就是foo(self, x),为什么要这么做呢?因为实例方法的调用离不开实例,我们需要把实例自己传给函数,调用的时候是这样的a.foo(x)(其实是foo(a,x))
类方法一样,只不过他传递的是类而不是实例,A.class_foo(x),注意这里的self和cls是可以替换别的参数,但是python约定的是这2个
对于静态方法其实和普通的方法一样,不需要对谁进行绑定,唯一的区别是调用的时候需要使用a.static_foo(x)或者A.static_foo(x)来调用

@author: xiaoq
'''
def foo(x):
    print "executing foo(%s)"%(x)

class A(object):
    def foo(self,x):
        print "executing foo(%s,%s)"%(self,x)

    @classmethod
    def class_foo(cls,x):
        print "executing class_foo(%s,%s)"%(cls,x)

    @staticmethod
    def static_foo(x):
        print "executing static_foo(%s)"%x

a=A()
foo(3)
a.foo(3)
a.class_foo(3)
A.class_foo(3)
a.static_foo(3)
A.static_foo(3)