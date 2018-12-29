#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' 该模块用于获取付费代理IP '''

import requests

# 代理服务器和端口
proxy_host = 'ip.16yun.cn'
proxy_port = '817'
# 代理隧道验证信息
proxy_user = 'xqm'
proxy_passwd = 'biosnkimdl'

# 代理主体
proxy_meta = 'http://%(user)s:%(pass)s@%(host)s:%(port)s' % {
    "host": proxy_host,
    "port": proxy_port,
    "user": proxy_user,
    "pass": proxy_passwd,
}
