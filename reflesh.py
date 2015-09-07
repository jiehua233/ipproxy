#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from base import Base

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

""" 定时刷新 """

class Reflesh(Base):

    def do(self):
        for i in range(4):
            key = "proxy_ip_ping_%s" % i
            self.ips = self.redis.zrange(key, 0, -1)
            print key, len(self.ips)
            self.reflsh(i)

    def reflsh(self, i):
        key = "proxy_ip_ping_%s" % i
        for ip in self.ips:
            p = ip.split(":")
            try:
                start = time.time()
                if self._ping(p[0], p[1]):
                    duration = time.time() - start
                    self.redis.zadd(key, duration, ip)
                    print "add"
                else:
                    self.redis.zrem(key, ip)
                    print "del"

            except Exception, e:
                print e
