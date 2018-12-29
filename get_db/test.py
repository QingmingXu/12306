#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' 该模块用于测试Python与Redis交互 '''

import json
from get_db.get_redis import RedisDB

# 创建几个字典，序列化后存到Redis的list中
train = {
           "arrive_order": "15",
           "arrive_station": "广州南",
           "arrive_time": "23:38",
           "start_order": "01",
           "start_station": "上海虹桥",
           "start_time": "15:25",
           "train_no": "G1305",
           "use_time": "08:13",
           "seat_type": "OM9"
}
'''
if RedisDB('114.116.37.42', 6379, 'xqm1997').redis_object.exists('12306:20181217:上海:广州'):
        RedisDB.redis_object.delete('12306:20181217:上海:广州')
RedisDB().insert_redis_list(key='12306:20181217:上海:广州', value=json.dumps(train))
'''
redisDB = RedisDB('114.116.37.42', 6379, 'xqm1997')
if redisDB.redis_object.exists('12306:20181217:上海:广州'):
    redisDB.redis_object.delete('12306:20181217:上海:广州')
redisDB.insert_redis_list(key='12306:20181217:上海:广州', value=json.dumps(train, ensure_ascii=False))
print(redisDB.redis_object.lindex('12306:20181217:上海:广州', 0))