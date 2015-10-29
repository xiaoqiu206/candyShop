#coding=utf-8
'''
Created on 2015年10月15日
用*args和**kwargs只是为了方便,并没有强制使用他们
@author: xiaoq
'''
# 当你不确定你的函数里将要传递多少参数时你可以使用*args.例如,他可以传递任意数量的参数:
def print_everything(*args):
    for count, thing in enumerate(args):
        print '{0}. {1}'.format(count, thing)

print_everything('apple', 'banana', 'cabbage')

# 相似的,**kwargs允许你使用没有事先定义的参数名:
def table_things(**kwargs):
    for name, value in kwargs.items():
        print '{0} = {1}'.format(name, value)
        
table_things(apple='fruit', cabbage='vagetable')

# 你也可以混着用.命名参数首先获得参数值然后所有的其他参数都传递给*args和**kwargs.命名参数在列表的最前端.例如:
# def table_things(titlestring, **kwargs):
# *args和**kwargs可以同时在函数的定义中,但是*args必须在**kwargs前面.
# 当调用函数时你也可以用*和**语法,例如:
def print_three_things(a, b, c):
    print 'a={0}, b={1}, c={2}'.format(a, b, c)

mylist = ['aardvark', 'baboon', 'cat']
print_three_things(*mylist)    # a=aardvark, b=baboon, c=cat

# 就像你看到的一样,它可以传递列表(或者元组)的每一项并把它们解包,注意必须与他们在函数里的参数相吻合.
# 当然,你也可以在函数定义或者函数调用时用*.
