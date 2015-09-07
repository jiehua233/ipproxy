#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import redis
import time

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
        pool = redis.ConnectionPool(host="127.0.0.1", port=6379)
        self.redis = redis.StrictRedis(connection_pool=pool)

    def ping(self):
        for ip in self.ips:
            try:
                start = time.time()
                if self._ping(ip["ip"], ip["port"]):
                    duration = time.time() - start
                    key = "proxy_ip_ping_%s" % ip["t"]
                    self.redis.zadd(key, duration, "%s:%s" % (ip["ip"], ip["port"]))
                    print "done"
            except Exception, e:
                print e

    def _ping(self, ip, port):
        print "ping: %s:%s" % (ip, port)
        #url = "http://cn.bing.com"
        url = "http://www.baidu.com"
        #url = "http://www.1yyg.com"
        proxies = {
            "http": "http://%s:%s" % (ip, port),
        }
        try:
            r = requests.get(url, proxies=proxies, timeout=self.timeout)
            if r.status_code == requests.codes.ok:
                return True
        except Exception, e:
            print e

        return False
