# coding=utf-8
'''
Created on 2015年8月26日

@author: Administrator
'''
# 因为浮点数不精确,所以使用Decimal,公式中出现的浮点数也都转换为Decimal
from decimal import Decimal
import msvcrt as m


def main():
    '主方法'
    # 第一步
    print 'Generator:'
    q = Decimal(raw_input('please input q(kJ): '))
    t = Decimal(raw_input('please input t(s): '))
    M = Decimal(raw_input('please input M(kg): '))

    Ti = q * t / M / Decimal('4.3') + 293
    Ma = q * t / Decimal('1145.76')

    print 'The temperature of ammonia gas in generator Ti: %.3f K' % Ti
    print 'The mass of the released ammonia gas Ma: %.3f Kg' % Ma
    print 'Press any key to continue...\n'
    m.getch()

    # 第二步
    print 'Condener:'
    Tj = Ti - Decimal('1145.76') / Decimal('1.624')
    print 'The ammonia liquid temperature in condenser Tj: %.3f K' % Tj
    print 'Press any key to continue...\n'
    m.getch()

    # 第三步
    print 'Evaporator:'
    Qe = q * t * Decimal('1248.59') / Decimal('1145.76')
    print 'The refrigerating capacity Qe: %.3f KJ' % Qe
    Te = t * Decimal('1248.59') / Decimal('4.708') + Tj
    print 'The ammonia vapor temperature in evaporator Te: %.3f K' % Te
    print 'Press any key to restart...\n'
    m.getch()

if __name__ == '__main__':
    # 将主方法加入无限循环
    while True:
        main()
