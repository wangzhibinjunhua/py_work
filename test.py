
# -*- coding: utf-8 -*-
# @Time    : 2016-12-07 16:00
# @Author  : wzb<wangzhibin_x@foxmail.com>

import configparser
import  binascii
config = configparser.ConfigParser()
config.set('info', 'totalnum', 1)
config.write(open('v.cfg', 'w'))