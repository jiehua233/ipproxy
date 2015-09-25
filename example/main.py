#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""代理IP使用范例

"""

import redis
import random
import requests


pool = redis.ConnectionPool(host="127.0.0.1", port=6379, db=1)
r = redis.StrictRedis(connection_pool=pool)
key = "proxy_ip_ping_3" # 暂时使用高匿名代理
timeout = 20  # 连接超时


def main():
    url = "http://www.baidu.com"
    retries = 0
    while True:
        proxies = getproxy(retries + 1)
        try:
            r = requests.get(url, proxies=proxies, timeout=timeout)
            if r.status_code == requests.codes.OK:
                print r.text
                break

        except Exception, e:
            print e

        print "fail! and retrying..."
        retries += 1
        if retries > 10:
            print "fail too many times"
            break


def getproxy(weight):
    # 根据权重获取随机代理ip, weight : [1...10]
    # 代理IP在redis中以sorted set存储, weight越大,ip质量越差
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
