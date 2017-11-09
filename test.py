
# -*- coding: utf-8 -*-
# @Time    : 2016-12-07 16:00
# @Author  : wzb<wangzhibin_x@foxmail.com>


import  binascii
sn='QD011738A002445'
cmd='0bff01514430313137333841303032343435'
print(type(cmd))
print(cmd[6:36])
if cmd.startswith('0bff') and len(cmd) == 36:
    re_sn = cmd[6:36]
    if re_sn == bytes.decode((binascii.b2a_hex(sn.encode()))):
        print(123)
