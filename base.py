#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis
import json


import sys
reload(sys)
sys.setdefaultencoding("utf-8")

"""
IP struct:
    ip = {
        "ip": "127.0.0.1",
        "port": "8888",
        "info": "XXXXX",
        "t": 1,     # type, 1: 透明, 2: 匿名, 3: 高匿名
    }

"""

class Base:

    ips = []
    timeout = 6
    redis = None

    def __init__(self):
        pool = redis.ConnectionPool(host="127.0.0.1", port=6379, db=1)
        self.redis = redis.StrictRedis(connection_pool=pool)

    def save(self, key):
        try:
            self.get()
            print len(self.ips)
            self.redis.set(key, json.dumps(self.ips))
            for ip in self.ips:
                self.redis.sadd("proxy_ip_%s" % ip["t"], "%s:%s" % (ip["ip"], ip["port"]))
        except Exception, e:
            print e

    def get(self):
        pass

