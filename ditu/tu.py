#coding=utf-8
'''
Created on 2016年1月17日
图算法,最短路径
@author: xiaoq
'''
graph = {'A': ['B', 'C'],
             'B': ['C', 'D'],
             'C': ['D'],
             'D': ['C'],
             'E': ['F'],
             'F': ['C']}


def find_shortest_path(graph, start, end, path=[]):
    