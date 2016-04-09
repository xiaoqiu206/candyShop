# coding=utf-8
'''
Created on 2016年3月13日
冒泡算法
@author: xiaoq
'''


def maopao(desc_list):
    for index in range(0, len(desc_list) - 1):
        for each in range(0, len(desc_list) - index - 1):
            if desc_list[each] > desc_list[each + 1]:
                desc_list[each], desc_list[
                    each + 1] = desc_list[each + 1], desc_list[each]

    return desc_list


desc_list = [1, 4, 7, 3, 1, 524, 4756, 568,
             13, 413, 64, 15, 3, 6537, 1, 53, 15]
# print maopao(desc_list)
desc_list.sort(reverse=False)
print desc_list