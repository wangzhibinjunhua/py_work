# -*- coding: utf-8 -*-
# @Time    : 2017-11-13 14:40
# @Author  : wzb<wangzhibin_x@foxmail.com>
import urllib.request

# 网址
url = "http://www.bbs.nga.cn/thread.php?fid=-7"

# 请求
request = urllib.request.Request(url)

# 爬取结果
response = urllib.request.urlopen(request)

data = response.read()

# 设置解码方式
data = data.decode('utf-8','ignore')
print(111)
# 打印结果
print(data)
print(22)

# 打印爬取网页的各类信息

print(type(response))
print(response.geturl())
print(response.info())
print(response.getcode())