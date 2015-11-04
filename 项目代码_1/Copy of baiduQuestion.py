# coding=utf-8
'''
Created on 2015年8月17日
Ca = 0.34
C = Cr - Ca
Q = 60 * m * (Cr - Ca) / 0.66
W = Q * T
@author: Administrator
'''
from decimal import Decimal


def main():
    Ca = Decimal('0.34')
    Cr = Decimal(raw_input('please input Cr: '))
    m = Decimal(raw_input('please input m : '))
    C = Cr - Ca
    if C < Decimal('0.06'):
        print 'gas-emission scope error'
    else:
        Q = 60 * m * C / Decimal('0.66')
        print 'Q = %s' % Q
        T = Decimal(raw_input('please input T : '))
        W = Q * T
        print 'W = %s' % W
        raw_input('program finished, press any key to exit')

if __name__ == '__main__':
    main()
