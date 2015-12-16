#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author   jiehua233@gmail.com
# @site     http://chenjiehua.me
# @date     2015-12-15
#

from crawler.daily import CZ88, KuaiDaiLi
from crawler.hourly import KuaiDaiLi2, XiCiDaiLi, IP66, \
    IP66API, IP002, CNProxy, CNProxyForeign

class Crawler:
    """ Crawl the public proxy ip from the Internet. """

    @classmethod
    def run(cls):
        proxyip = []
        for source in [CNProxy, CNProxyForeign, IP66, IP66API, IP002, \
                       XiCiDaiLi, KuaiDaiLi2, CZ88, KuaiDaiLi, IP002]:
            instance = source()
            print instance
            proxyip.extend(instance.crawl())

        return proxyip
