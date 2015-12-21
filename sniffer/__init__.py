#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author   jiehua233@gmail.com
# @site     http://chenjiehua.me
# @date     2015-12-16
#

import operator
import redis

from sniffer.validate import Validator
from etc.config import SNIFFER
from etc.logger import logger

class Sniffer:
    """ Validate the proxy ip. """

    def __init__(self):
        self.proxy_type = sorted(SNIFFER['PROXY_TYPE'], reverse=True)
        self.validator = Validator()
        self.redis = None

    def run(self, proxyips):
        result = {}
        proxy_set = self.classify(proxyips)
        for proxy_type in self.proxy_type:
            proxy_list = list(proxy_set.get(proxy_type, set()))
            logger.info('sniffer start, proxy_type: %s, proxy_ip: %s', proxy_type, len(proxy_list))
            result[proxy_type] = self.validator.run_in_multiprocess(proxy_list)
            logger.info('sniffer finish, proxy_type: %s, avail_ip: %s', proxy_type, len(result[proxy_type]))

        if SNIFFER['OUTPUT']:
            try:
                self.save2file(result)
            except Exception as e:
                logger.error("Write file fail, error: %s", e)

        if SNIFFER['BACKEND'] != '':
            try:
                self.redis = redis.StrictRedis(*SNIFFER['BACKEND'].split(':'))
                self.redis.ping()
            except Exception as e:
                logger.error("Backend redis error: %s", e)
                return

            self.reflesh_redis()
            self.save2redis(result)

    def save2file(self, result):
        """ 保存到文件 """
        for proxy_type in result:
            proxy_list = sorted(result[proxy_type].iteritems(), key=operator.itemgetter(1))
            with open('./data/ipproxy-%s.txt' % proxy_type, 'wb') as f:
                for ip in proxy_list:
                    f.write("%s\t%s\n" % (ip[0], ip[1]))

    def save2redis(self, result):
        """ 保存到redis """
        for proxy_type in self.proxy_type:
            key = '%s%s' % (SNIFFER['KEY_PREFIX'], proxy_type)
            for proxy_ip in result[proxy_type]:
                self.redis.zadd(key, result[proxy_type][proxy_ip], proxy_ip)

    def reflesh_redis(self):
        for proxy_type in self.proxy_type:
            key = '%s%s' % (SNIFFER['KEY_PREFIX'], proxy_type)
            proxy_list = self.redis.zrange(key, 0, -1)
            result = self.validator.run_in_multiprocess(proxy_list)
            # 删除过期数据
            for proxy_ip  in (set(proxy_list) - set(result.keys())):
                self.redis.zrem(key, proxy_ip)

            # 更新数据
            for proxy_ip in result:
                self.redis.zadd(key, result[proxy_ip], proxy_ip)

    def classify(self, proxyip):
        """ 根据匿名程度对ip进行分类 """
        result = {}
        for i in range(4):
            result.setdefault(i, set())

        for ip in proxyip:
            ip_port = "%(ip)s:%(port)s" % ip
            try:
                result[int(ip['type'])].add(ip_port)
            except Exception as e:
                print e
                print ip['ip'], ip['port'], ip['type']

        return result
