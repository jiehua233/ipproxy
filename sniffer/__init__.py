#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author   jiehua233@gmail.com
# @site     http://chenjiehua.me
# @date     2015-12-16
#

import redis

from sniffer.validate import Validator
from etc.config import SNIFFER, KEY_PREFIX

class Sniffer:
    """ Validate the proxy ip. """

    def __init__(self):
        self.proxy_type = sorted(SNIFFER['PROXY_TYPE'], reverse=True)
        self.validate = Validate()

    def run(self, proxyip):
        proxy_set = self.classify(proxyip)
        result = self.validate(proxy_set)
        if SNIFFER['OUTPUT']:
            self.save2file(result)

        if SNIFFER['BACKEND'] != '':
            self.save2redis(result)

    def validate(self, proxy_set):
        result = {}
        for proxy_type in self.proxy_type:
            proxy_list = list(proxy_set.get(proxy_type, set()))
            result[proxy_type] = validator.run_in_multiprocess(proxy_list)

        return result

    def save2file(self, result):
        """ 保存到文件 """
        for proxy_type in result:
            proxy_list = sorted(result[proxy_type].iteritems(), key=operator.itemgetter(1))
            with open('./data/ipproxy-%s.txt' % proxy_type) as f:
                for ip in proxy_list:
                    f.write("%s\t%s\n" % ip[0], ip[1])

    def save2redis(self, result):
        """ 保存到redis """
        self.redis = redis.StrictRedis(*SNIFFER['BACKEND'].split(':'))
        # TODO

    def classify(self, proxyip):
        """ 根据匿名程度对ip进行去重分类 """
        result = {}
        for i in range(4):
            result.setdefault(i, set())

        for ip in proxyip:
            ip_port = "%(ip)s:%(port)s" % ip
            result[int(ip['type'])].add(ip_port)

        return result
