# coding=utf-8
"""

"""


import os

info = os.popen("systeminfo")
print info.read().decode("gbk")