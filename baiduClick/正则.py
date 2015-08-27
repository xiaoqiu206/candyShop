# coding=utf-8
'''
Created on 2015年8月21日
用正则表达式匹配出input的name和value
@author: Administrator
'''
import re
# from memory_profiler import profiler


# @profile
def f1():
    '匹配1.html中input的name和value'
    # 读取1.html的内容
    html = file('1.txt', 'r').read()

    # 获取的是id='index-form'的input
    # 匹配整个form标签,python的re.findall()方法返回的是列表,所以form是包含一个元素的列表
    forms = re.findall(r'<form[^>]+>.+</form>', html)
    form = forms[0]
    # print form  # 打印出来就是整个form标签
    # print re.search(r'(?P<name>\S+)"\svalue="(?P<value>.*)"', form).groupdict()
    # 获取action
    action_str = re.findall(r'action="[^>]+?"', form)[0]
    print action_str  # 结果是 action="/from=844b/s" 需要再字符串处理

    # 获取input的name和value
    # 先获取input
    inputs = re.findall(r'<input[^<]+/>', form)
    # 遍历每个input,获取name和value
    name_value = {}
    for each in inputs:
        # print each
        m = re.search(
            r'name="(?P<name>\S+)"\svalue="(?P<value>.*)"', each)
        p = m.groupdict()
        name_value[p['name']] = p['value']

    print name_value


def f4():
    '匹配name-value'
    html = file('1.txt', 'r').read()
    forms = re.findall(r'<form[^>]+>.+</form>', html)
    form = forms[0]
    m = re.match(
        r'<input[^<]+name="(?P<name>\S+)"\svalue="(?P<value>.*)"/>', form)
    print m.groupdict()


def f2():
    '匹配2.html中input的name和value'
    pass


def f3():
    '匹配1.html中input的name和value'
    pass


if __name__ == '__main__':
    #     f4()
    f1()
