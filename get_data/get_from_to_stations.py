#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
该模块最终获得两个列表：from_to_station_name_list以及from_to_station_code_list，
from_to_station_name_list里面的每一个元素都是：始发站-终点站
from_to_station_code_list里面的每一个元素都是：始发站代码-终点站代码
'''

import json
import re
from get_data.stations import stations_dict

# 打开train_list.txt,并且把json转化为Python字典
with open('E:\\scarpy_12306\\get_data\\train_list.txt', 'rb') as f:
    f_dict = json.load(f)

# 选取样本，获得全国的始发站-终点站，9472个
list = []
sample_dict = f_dict['2018-12-20']
for v in sample_dict.values():
    for d in v:
        list.append(d['station_train_code'])

for_a_short_time_list = []
for n in list:
    for_a_short_time_list.append(re.findall('\w+-\w+.*\)$', n))

from_to_station_name_list = []
for n in for_a_short_time_list:
    from_to_station_name_list.append(n[0])

count = 0
from_to_station_code_list = []
for n in from_to_station_name_list:
    from_station_name = n.split('-')[0]
    not_available_to_station_name = n.split('-')[1]
    if ' ' in not_available_to_station_name:
        to_station_name = not_available_to_station_name.split()[0] \
                          + not_available_to_station_name.split()[1][0:len(not_available_to_station_name.split()[1])-1]
    else:
        to_station_name = not_available_to_station_name[0:len(not_available_to_station_name)-1]
    if from_station_name in stations_dict.keys() and to_station_name in stations_dict.keys():
        from_station_code = stations_dict[from_station_name]
        to_station_code = stations_dict[to_station_name]
        from_to_station_code_list.append(from_station_code + '-' + to_station_code)

# 去重
from_to_station_code_list = set(from_to_station_code_list)
from_to_station_code_list = [i for i in from_to_station_code_list]

'''
print(from_to_station_code_list)
print(len(from_to_station_code_list))
'''




