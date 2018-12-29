#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' 获取Redis '''

import redis

# 自定义的Redis数据库类
class RedisDB(object):
    # 构造方法
    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.redis_pool = redis.ConnectionPool(host=host, port=port, password=password, db=1)
        self.redis_object = redis.StrictRedis(connection_pool=self.redis_pool)

    # 从右往左的往Redis的list中加入数据
    def insert_redis_list_left(self, key, value):
        self.redis_object.lpush(key, value)

    # 从左往右的往Redis的list中加入数据
    def insert_redis_list_right(self, key, value):
        self.redis_object.rpush(key, value)

    # 往Redis中加入string类型的数据，支持设置过期时间
    def insert_redis_string_ex(self, key, time, value):
        self.redis_object.setex(key, time, value)

    # 往Redis中加入string类型的数据
    def insert_redis_string(self, key, value):
        self.redis_object.set(key, value)

    def __str__(self):
        return 'redis:host:{} port:{}'.format(self.host, self.port)




