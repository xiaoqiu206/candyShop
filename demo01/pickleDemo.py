# coding=utf-8
'''
Created on 2015年4月11日
pickle的小demo
@author: Administrator
'''
try:
    import cPickle as pickle
except:
    import pickle

'''
a = 'orange'
f1 = open('1.pk','wb')
pickle.dump(a, f1, True)
'''
f2 = file('1.pk','rb')
b = pickle.load(f2)
c = pickle.load(f2)
print b, c



