#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import requests
from base import Base

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

""" 定时刷新 """

class Validate(Base):

    def reflesh(self):
        # 优先处理高匿名代理
        for i in range(4)[::-1]:
            key = "proxy_ip_ping_%s" % i
            ips = self.redis.zrange(key, 0, -1)
            print key, len(ips)
            for ip in ips:
                try:
                    start = time.time()
                    if self._ping(ip):
                        duration = time.time() - start
                        self.redis.zadd(key, duration, ip)
                        print "reflesh in sorted set"
                    else:
                        self.redis.zrem(key, ip)
                        print "del from sorted set"

                except Exception, e:
                    print e

            # 只检测高匿名代理ip
            break

    def ping(self):
        # 优先处理高匿名代理
        for i in range(4)[::-1]:
            skey = "proxy_ip_%s" % i
            zkey = "proxy_ip_ping_%s" % i
            ips = self.redis.smembers(skey)
            print skey, len(ips)
            for ip in ips:
                try:
                    start = time.time()
                    if self._ping(ip):
                        duration = time.time() - start
                        self.redis.zadd(zkey, duration, ip)
                        print "add to sorted set"
                    else:
                        self.redis.srem(skey, ip)
                        print "del from set"

                except Exception, e:
                    print e

            # 只检测高匿名代理ip
            break

    def _ping(self, ip_port):
        print "ping: %s" % ip_port
        #url = "http://cn.bing.com"
        url = "http://www.baidu.com"
        #url = "http://www.1yyg.com"
        proxies = {
            "http": "http://%s" % ip_port,
        }
        try:
            r = requests.get(url, proxies=proxies, timeout=self.timeout)
            if r.status_code == requests.codes.ok:
                return True

        except:
            pass
        #except Exception, e:
        #    print e

        return False
