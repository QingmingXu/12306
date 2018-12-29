#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' 该模块将用于生成stations.py '''

import requests
import re

#关闭https证书验证警告
requests.packages.urllib3.disable_warnings()
# 存有12306的城市名和城市代码的js文件URL
city_code_url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9085'
# 发送请求
response = requests.get(city_code_url, verify=False)
# 正则表达式，用于匹配站名和站名对应的代码
pattern = u'([\u4e00-\u9fa5]+)\|([A-Z]+)'
# 该列表的元素为元组，元组中的元素分别为站名和站名对应的代码
result = re.findall(pattern, response.text)
# 转化为字典
station = dict(result)
