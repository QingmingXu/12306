#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' 该模块用于获取免费的代理IP '''

import requests
import re
import random
from get_data.get_headers_list import user_agent_list

# 关闭HTTPS证书警告
requests.packages.urllib3.disable_warnings()
def check_ip(ip):
    test_url = 'https://www.baidu.com'
    proxy = {'http': ip}
    user_agent = random.choice(user_agent_list)
    headers = {'User-Agent': user_agent}
    try:
        response = requests.get(test_url, headers=headers, proxies=proxy, verify=False, timeout=5)
        #time.sleep(2)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False

url = 'https://www.xicidaili.com/nn/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 '}
response = requests.get(url, headers=headers, verify=False)
reg_for_ip = r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>\s*?<td>(\d*)</td>'
match = re.compile(reg_for_ip)
result = re.findall(match, response.text)

# 未经检查的IP列表
ip_list_sample = []
for r in result:
    ip_list_sample.append('http://' + r[0] + ':' + r[1])

# 验证后的IP列表
ip_list_reliable = []
for ip in ip_list_sample:
    if check_ip(ip):
        ip_list_reliable.append(ip)

'''
for n in ip_list_reliable:
    print(n)
'''