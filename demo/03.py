#coding=utf-8
'''
Created on 2015年10月22日

@author: xiaoq
'''
def mymax(num1,*numr):
    print numr
    nummax=num1
    for i in numr:
        if i>nummax:
            nummax=i
    return nummax

num1=1
num2=[1,23,4,6,87,9]
max1=mymax(num1,*num2)
print(max1)