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
    try:
        Cr = Decimal(raw_input('please input Cr: '))
    except:
        print 'wrong number format !'
        raw_input('progarm stopped,press any key to exit')
        return

    try:
        m = Decimal(raw_input('please input m : '))
    except:
        print 'wrong number format'
        raw_input('progarm stopped,press any key to exit')
        return

    C = Cr - Ca
    if C < Decimal('0.06'):
        print 'gas-emission scope error'
        raw_input('progarm finished,press any key to exit')
    else:
        Q = 60 * m * C / Decimal('0.66')
        print 'Q = %s' % Q

        try:
            T = Decimal(raw_input('please input T : '))
        except:
            print 'wrong number format !'
            raw_input('progarm stopped,press any key to exit')
            return

        W = Q * T
        print 'W = %s' % W
        raw_input('program finished, press any key to exit')

if __name__ == '__main__':
    main()
