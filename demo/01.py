# coding=utf-8
'''
Created on 2015年10月22日
Assume s is a string of lower case characters.
Write a program that prints the longest substring of s in which the letters occur in alphabetical order. 
For example, if s = 'azcbobobegghakl', 
then your program should print Longest substring in alphabetical order is: beggh In the case of ties, 
print the first substring. For example, if s = 'abcbcd', 
then your program should print Longest substring in alphabetical order is: abc  
Note: This problem is fairly challenging. 
We encourage you to work smart. If you've spent more than a few hours on this problem, 
we suggest that you move on to a different part of the course. 
If you have time, come back to this problem after you've had a break and cleared your head.
找出一段小写字符串中按照字母表从低到高排列的最长的部分
@author: xiaoq
'''
a = 'azcbobobegghakl'
isbig_list = []  # 每个字母对应0或1(不包括第一个),如果比前面的大,则标记为1,否则0
for k, v in enumerate(a):
    if k == 0:
        continue
    if v >= a[k - 1]:
        isbig_list.append('1')
    else:
        isbig_list.append('0')

isbig_str = ''.join(isbig_list)  # 将包含0和1的列表组合成字符串
list_with_one = isbig_str.split('0')  # 字符串用0分隔
biggest = max(list_with_one)  # 包含最长的1的部分
start = isbig_str.find(max(list_with_one))  # 最长的1部分的索引
print a[start: start + len(biggest) + 1]  # 按照索引获取字符串中符合条件的最长部分
