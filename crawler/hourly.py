#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author   jiehua233@gmail.com
# @site     http://chenjiehua.me
# @date     2015-12-15
#

import sys
import urlparse

from crawler.base import Base

reload(sys)
sys.setdefaultencoding("utf-8")

"""实时获取"""
class KuaiDaiLi2(Base):
    """ www.kuaidaili.com """

    def crawl(self):
        base = "http://www.kuaidaili.com/proxylist/"
        proxyip = []
        for i in range(1, 11):
            proxyip.extend(self.get(urlparse.urljoin(base, str(i))))

        return proxyip

    def parse(self, soup):
        result = []
        for s in soup.find("table").find_all("tr")[1:]:
            try:
                d = s.find_all("td")
                ip = {
                    "ip": d[0].string,
                    "port": d[1].string,
                    "info": d[5].string,
                    "type": 0,
                }
                if d[2].string == "透明":
                    ip["type"] = 1
                elif d[2].string == "匿名":
                    ip["type"] = 2
                elif d[2].string == "高匿名":
                    ip["type"] = 3

                result.append(ip)

            except Exception as e:
                print e

        return result


class XiCiDaiLi(Base):
    """ www.xicidaili.com """

    def crawl(self):
        base = "http://www.xicidaili.com"
        proxyip = []
        headers = {
            "Host": "www.xicidaili.com",
            "Referer": "http://www.xicidaili.com",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36",
        }
        for u in ["nn", "nt", "wn", "wt"]:
            proxyip.extend(self.get(urlparse.urljoin(base, u), headers=headers))

        return proxyip

    def parse(self, soup):
        result = []
        for s in soup.find("table").find_all("tr")[1:]:
            try:
                d = s.find_all("td")
                ip = {
                    "ip": d[2].string,
                    "port": d[3].string,
                    "info": "",
                    "type": 0,
                }
                info = d[4].find("a")
                if info:
                    ip["info"] = info.string

                if d[5].string == "透明":
                    ip["type"] = 1
                elif d[5].string == "匿名":
                    ip["type"] = 2
                elif d[5].string == "高匿":
                    ip["type"] = 3

                result.append(ip)

            except Exception as e:
                print e

        return result


class IP66(Base):
    """ www.66ip.cn """

    def get(self):
        base = "http://www.66ip.cn"
        proxyip = []
        for i in range(1, 11):
            proxyip.extend(self.get(urlparse.urljoin(base, "%s.html" % i)))

        return proxyip

    def parse(self, soup):
        result = []
        for s in soup.find_all("table")[2].find_all("tr")[1:]:
            try:
                d = s.find_all("td")
                ip = {
                    "ip": d[0].string,
                    "port": d[1].string,
                    "info": d[2].string,
                    "type": 0,
                }
                if d[3].string == "透明":
                    ip["type"] = 1
                elif d[3].string == "匿名":
                    ip["type"] = 2
                elif d[3].string == "高匿代理":
                    ip["type"] = 3

                result.append(ip)

            except Exception as e:
                print e

        return result


class CNProxy(Base):
    """ http://cn-proxy.com """

    def crawl(self):
        base = "http://cn-proxy.com"
        proxyip = self.get(base)
        return proxyip

    def parse(self, soup):
        result = []
        for s in soup.find_all("table"):
            for t in s.find_all("tr")[2:]:
                try:
                    ip = self._parse(t.find_all("td"))
                    result.append(ip)

                except Exception as e:
                    print e

        return result

    def _parse(self, d=[]):
        ip = {
            "ip": d[0].string,
            "port": d[1].string,
            "info": d[2].string,
            "type": 3,
        }
        return ip


class CNProxyForeign(CNProxy):
    """ http://cn-proxy.com/archives/218 """

    def crawl(self):
        base = "http://cn-proxy.com/archives/218"
        proxyip = self.get(base)
        return proxyip

    def _parse(self, d=[]):
        ip = {
            "ip": d[0].string,
            "port": d[1].string,
            "info": d[3].string,
            "type": 0,
        }
        if d[2].string == "透明":
            ip["t"] = 1
        elif d[2].string == "匿名":
            ip["t"] = 2
        elif d[2].string == "高度匿名":
            ip["t"] = 3

        return ip
