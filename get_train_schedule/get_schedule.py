#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' 该模块主要用于获取列车时刻表 '''

import requests
import json
import random
from datetime import datetime
from get_data.stations import stations_dict
from get_data.get_free_ip import ip_list_reliable
from get_data.get_charge_ip import proxy_meta
from get_data.get_headers_list import user_agent_list
from get_data.get_from_to_stations import from_to_station_code_list, from_to_station_name_list
from get_db.get_redis import RedisDB
'''
需要用到以下两个接口：
1：https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2018-12-19&leftTicketDTO.from_station=SHH&leftTicketDTO.to_station=BJP&purpose_codes=ADULT
2：https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no=5500000G1201&from_station_telecode=SHH&to_station_telecode=VNP&depart_date=2018-12-19
接口1会经常变化，需要注意
'''
'''
用于写入到文本
info = '{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(station_train_code, today, station_name, arrive_time, start_time, station_no, seat_type)
with open('E:\\scarpy_12306\\get_train_schedule\\train_schedule.txt', 'a') as f:
f.write(info)
'''

# 将stations_dict的键值反转，形成新的字典，形如'VAP': '北京北'
city_dict = {v: k for k, v in stations_dict.items()}
# 关闭HTTPS证书警告
requests.packages.urllib3.disable_warnings()
# 获取今天的日期，格式形如：2018-12-19
today = str(datetime.now()).split(' ')[0]
# 获取今天的日期，格式形如：20181219
date = today.split('-')[0] + today.split('-')[1] + today.split('-')[2]
# 实例化RedisDB
redisDB = RedisDB('114.116.37.42', 6379, 'xqm1997')

def get_data_from_12306_and_write_in_db():
    # 一级循环，遍历全国始发站-终点站对应的代码，形如：SHH-VUQ
    for n in from_to_station_code_list:
        # 构造请求接口1的的URL
        from_station = n.split('-')[0]
        to_station = n.split('-')[1]
        url_1 = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?'\
                'leftTicketDTO.train_date={}&'\
                'leftTicketDTO.from_station={}&'\
                'leftTicketDTO.to_station={}&'\
                'purpose_codes=ADULT'.format(today, from_station, to_station)
        # 代理
        proxies = dict()
        proxies['http'] = random.choice(ip_list_reliable)
        #proxies['http'] = proxy_meta
        # USER-AGENT
        headers = dict()
        headers['User-Agent'] = random.choice(user_agent_list)
        #  向请求接口1发送请求
        response_1 = requests.get(url_1, headers=headers, proxies=proxies, verify=False)
        # 打印响应的类型
        print(response_1.headers["Content-Type"])
        # 当响应的类型为JSON时，打印响应的text，否则打印错误页面
        if response_1.headers["Content-Type"] == 'application/json;charset=UTF-8':
            print(response_1.text)
        else:
            print("错误页面。。。")
        # 当响应的类型不是JSON时，跳出当前循环，进入下次循环，即循环下一个始发站-终点站对应的代码
        if response_1.headers["Content-Type"] != 'application/json;charset=UTF-8':
            continue
        # 处理出现未完结字符串的情况
        if response_1.text[-1] != '}' and '"httpstatus":200,"messages":"","status":true' not in response_1.text:
            #response_1.text = response_1.text + '"]},"httpstatus":200,"messages":"","status":true}'
            continue
        '''
        关键内容,result_1是一个列表，列表中的每个元素类似于：|预订|6k0000D93200|D933|ZWQ|AOH|IZQ|AOH|19:24|06:50|11:26|N|
        aaInSA5kfxb2z7eNkIr8a3r%2FJC4LJZVeBMgctXcmuRDORNN3|20181221|3|Q6|05|09|1|0||无|||||||||无|||无|A0F0O0|AFO|0
        '''
        result_1 = json.loads(response_1.text)["data"]["result"]
        # 创建一个空列表，用于存放train_data_for_redis_1
        list_for_redis_1 = []
        # 生成键，key：12306:日期:出发站:到达站
        key_for_redis_1 = '12306:{}:{}:{}'.format(date, city_dict[from_station], city_dict[to_station])
        # 二级循环，循环result_1的元素
        for r in result_1:
            if '列车停运' in r:
                continue
            # 当出现未完结字符串并完成拼接后，result_1中的最后一个元素大机率不可用。正常情况下，r.split('|')的长度为38或37
            #if len(r.split('|')) < 37:
                #continue
            # r是一个列表，一般有38个元素，特殊情况下37个元素
            r = r.split('|')
            train_no = r[2]
            station_train_code = r[3]
            from_station_telecode = r[4]
            to_station_telecode = r[5]
            seat_type = r[35]
            use_time = r[10]
            arrive_order = r[17]
            start_order = r[16]
            arrive_time = r[9]
            start_time = r[8]
            if len(r) == 36:
                train_no = r[1]
                station_train_code = r[2]
                from_station_telecode = r[3]
                to_station_telecode = r[4]
                seat_type = r[34]
                use_time = r[9]
                arrive_order = r[16]
                start_order = r[15]
                arrive_time = r[8]
                start_time = r[7]
            # 在二级循环结束时把数据存入redis，key：12306:日期:出发站:到达站，value为一个列表
            if from_station_telecode in city_dict.keys() and to_station_telecode in city_dict.keys():
                train_data_for_redis_1 = {}
                train_data_for_redis_1["arrive_order"] = arrive_order
                train_data_for_redis_1["arrive_station"] = city_dict[to_station_telecode]
                train_data_for_redis_1["arrive_time"] = arrive_time
                train_data_for_redis_1["start_order"] = start_order
                train_data_for_redis_1["start_station"] = city_dict[from_station_telecode]
                train_data_for_redis_1["start_time"] = start_time
                train_data_for_redis_1["train_no"] = station_train_code
                train_data_for_redis_1["use_time"] = use_time
                train_data_for_redis_1["seat_type"] = seat_type
                list_for_redis_1.append(train_data_for_redis_1)
            # 把数据存入redis，key：12306:no:日期:车次，value是一个列表
            # 生成键，key：12306:no:日期:车次
            key_for_redis_2 = '12306:no:{}:{}'.format(date, station_train_code)
            train_data_for_redis_2 = {}
            train_data_for_redis_2["first_station"] = from_station_telecode
            train_data_for_redis_2["last_station"] = to_station_telecode
            train_data_for_redis_2["train_code"] = train_no
            redisDB.insert_redis_string_ex(key=key_for_redis_2, time=259200,
                                        value=json.dumps(train_data_for_redis_2, ensure_ascii=False))
            # 构造请求接口2的URL
            url_2 = 'https://kyfw.12306.cn/otn/czxx/queryByTrainNo?'\
                    'train_no={}&'\
                    'from_station_telecode={}&'\
                    'to_station_telecode={}&'\
                    'depart_date={}'.format(train_no, from_station_telecode, to_station_telecode, today)
            # 代理
            proxies = dict()
            proxies['http'] = random.choice(ip_list_reliable)
            #proxies['http'] = proxy_meta
            # USER-AGENT
            headers = dict()
            headers['User-Agent'] = random.choice(user_agent_list)
            # 向请求接口2发送请求
            response_2 = requests.get(url_2, headers=headers, proxies=proxies, verify=False)
            result_2 = json.loads(response_2.text)["data"]["data"]
            # 创建一个空列表，用于存放train_data_for_redis_3
            list_for_redis_3 = []
            # 生成键，key：12306:日期:车次
            key_for_redis_3 = '12306:{}:{}'.format(date, station_train_code)
            # 三级循环
            for r in result_2:
                # 把数据存入redis，key：12306:日期:车次，value是一个列表
                train_data_for_redis_3 = {}
                train_data_for_redis_3["station_name"] = r['station_name']
                train_data_for_redis_3["pass_order"] = r['station_no']
                train_data_for_redis_3["arrive_time"] = r['arrive_time']
                train_data_for_redis_3["leave_time"] = r['start_time']
                list_for_redis_3.append(train_data_for_redis_3)
            redisDB.insert_redis_string_ex(key=key_for_redis_3, time=259200,
                                        value=json.dumps(list_for_redis_3, ensure_ascii=False))
        redisDB.insert_redis_string_ex(key=key_for_redis_1, time=432000,
                                    value=json.dumps(list_for_redis_1, ensure_ascii=False))
    print('数据采集完毕！')

if __name__ == '__main__':
    while True:
        try:
            pass
        except Exception as e:
            with open('./scrapy_12306.txt', 'a') as f:
                f.write('Exception:' + e + '\n')
