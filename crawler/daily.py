#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author   jiehua233@gmail.com
# @site     http://chenjiehua.me
# @date     2015-12-15
#

import sys
import urlparse
import requests

from bs4 import BeautifulSoup
from crawler.base import Base
from etc.logger import logger

reload(sys)
sys.setdefaultencoding("utf-8")

"""每日获取"""
class CZ88(Base):
    """ http://www.cz88.net/proxy/http_2.shtml """

    def crawl(self):
        base = "http://www.cz88.net/proxy/"
        proxyip = []
        pages = ["index.shtml"]
        pages.extend(["http_%d.shtml" % i for i in range(2, 11)])
        for page in pages:
            proxyip.extend(self.get(urlparse.urljoin(base, page), encoding="GBK"))

        return proxyip

    def parse(self, soup):
        result = []
        soup = soup.find("div", id="boxright").find_all("li")
        keys = ["ip", "port", "type", "info"]
        for s in soup[1:]:
            try:
                ip = {}
                for idx, val in enumerate(s.stripped_strings):
                    ip[keys[idx]] = val

                ip['type'] = 1
                result.append(ip)
            except Exception as e:
                logger.error('CZ88 parse error: %s', e)

        return result


class KuaiDaiLi(Base):
    """ http://blog.kuaidaili.com/ """

    def crawl(self):
        base = "http://blog.kuaidaili.com/"
        proxyip = []
        r = requests.get(base)
        if r.status_code  == requests.codes.ok:
            soup = BeautifulSoup(r.text, "html5lib")
            for s in soup.find_all("article")[:2]:
                proxyip.extend(self.get(s.find("a")["href"]))

        else:
            logger.error("KuaiDaiLi crawl root fail, HTTP Response Code: %s", r.status_code)

        return proxyip

    def parse(self, soup):
        result = []
        s = soup.find("div", class_="entry-content").find_all("p")
        for d in s[1].stripped_strings:
            try:
                rst = d.split(u"\xa0\xa0", 2)
                if len(rst) != 3:
                    continue

                ip = {
                    "ip": rst[0].split(":")[0],
                    "port": rst[0].split(":")[1],
                    "info": rst[2],
                }
                if rst[1] == "透明":
                    ip["type"] = 1
                elif rst[1] == "匿名":
                    ip["type"] = 2
                elif rst[1] == "高匿名":
                    ip["type"] = 3
                else:
                    ip["type"] = 0

                result.append(ip)

            except Exception, e:
                logger.error('KuaiDaiLi parse error: %s', e)

        return result


