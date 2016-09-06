#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author   jiehua233@gmail.com
# @site     http://chenjiehua.me
# @date     2015-12-21
#

"""代理IP使用范例

"""

import redis
import random
import requests


pool = redis.ConnectionPool(host="127.0.0.1", port=6379, db=0)
r = redis.StrictRedis(connection_pool=pool)
key = "ipproxy:3"   # 暂时使用高匿名代理
timeout = 20        # 连接超时


def main():
    url = "http://www.baidu.com"
    retries = 0
    while True:
        proxies = getproxy(retries + 1)
        print 'Using proxy:%s' % proxies
        try:
            r = requests.get(url, proxies=proxies, timeout=timeout)
            if r.status_code == requests.codes.OK:
                print r.text
                break

        except Exception as e:
            print e

        print "fail! and retrying..."
        retries += 1
        if retries > 10:
            print "fail too many times"
            break


def getproxy(weight):
    # 根据权重随机获取代理ip, weight : [1...10]
    # 代理IP在redis中以zset存储, weight越大,ip质量越差
    total = r.zcard(key)
    ips = r.zrange(key, 0, total/10*weight)
    # 获取全部代理IP
    # ips = r.zrange(key, 0, -1)
    proxies = {
        "http": "http://%s" % ips[random.randint(0, len(ips)-1)]
    }
    return proxies


if __name__ == "__main__":
    main()
