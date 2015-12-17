#!/usr/bin/env python
# -*- coding: utf-8 -*-

SNIFFER = {
    'PROCESS_NUM': 4,
    'THREAD_NUM': 500,
    'PROXY_TYPE': [0, 1, 2, 3],
    'TARGET': 'http://www.baidu.com',
    'TIMEOUT': 10,
    'OUTPUT': True,
    'BACKEND': 'localhost:6379',
    'KEY_PREFIX': 'ipproxy:',
}

LOGGER = {
    "PATH": './ipproxy.log'
}
