# coding=utf-8
"""

"""


def extendlist(val, li=[]):
    li.append(val)
    return li

list1 = extendlist(10)
print "list1 = %s" % list1  # [10]
list2 = extendlist(123,[])
list3 = extendlist('a')

print "list1 = %s" % list1  # [10, 'a']
print "list2 = %s" % list2  # [123]
print "list3 = %s" % list3  # [123,'a']