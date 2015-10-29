# coding=utf-8
'''
Created on 2015年10月29日

@author: xiaoq
'''


def isPrime(n):
    import math
    if n == 1:
        return False
    elif n < 4:
        return True
    elif n & 1 == 0:
        return False
    elif n < 9:
        return True
    elif n % 3 == 0:
        return False
    else:
        r = math.floor(math.sqrt(n))
        f = 5
        while f <= r:
            if n % f == 0:
                return False
            if n % (f + 2) == 0:
                return False
            f += 6
        return True

plist = []

import time

t1 = time.time()


def main1():
    for x in range(1, 2000000):
        if isPrime(x):
            plist.append(x)

    print sum(plist)

    print time.time() - t1


def main():
    nums = range(2, 2000000)
    length = len(nums)
    for i in xrange(length):
        if nums[i] == 0:
            continue
        # nums[i] is now a prime
        p = nums[i]
        # remove all a * nums[i]
        for j in xrange(i + p, length, p):
            nums[j] = 0
    return sum(nums)
print main()
print time.time() - t1
