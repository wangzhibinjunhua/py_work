
# -*- coding: utf-8 -*-
# @Time    : 2016-12-07 16:00
# @Author  : wzb<wangzhibin_x@foxmail.com>


import  binascii
cmd='1: 0x70E027F4313D, -63, Smart Basketball'
device_id = cmd[:1]
s = cmd.split(',')
print(s)
print(len(s))
device_rssi = s[1]
device_name = s[2]
