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
from etc.logger import logger

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
                logger.error('KuaiDaiLi2 parse error: %s', e)

        return result


class XiCiDaiLi(Base):
    """ www.xicidaili.com """

    def crawl(self):
        base = "http://www.xicidaili.com"
        proxyip = []
        headers = {
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
                logger.error('XiCiDaiLi parse error: %s', e)

        return result


class IP66(Base):
    """ www.66ip.cn """

    def crawl(self):
        base = "http://www.66ip.cn"
        proxyip = []
        for i in range(1, 11):
            proxyip.extend(self.get(urlparse.urljoin(base, "%s.html" % i), encoding='UTF-8'))

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
                logger.error('IP66 parse error: %s', e)

        return result


class IP66API(Base):
    """ http://www.66ip.cn/nm.html """

    def crawl(self):
        proxyip = []
        for c in range(3):
            # 普通代理IP
            pt = "http://www.66ip.cn/mo.php?tqsl=800"
            proxyip.extend(self.set_type(self.get(pt), 1))
            # 超级匿名
            nm = "http://www.66ip.cn/nmtq.php?getnum=800&anonymoustype=4&proxytype=2&api=66ip"
            proxyip.extend(self.set_type(self.get(nm), 3))
            for i in range(1, 4):
                # 透明，普匿，高匿
                nm = "http://www.66ip.cn/nmtq.php?getnum=800&anonymoustype=%s&proxytype=2&api=66ip" % i
                proxyip.extend(self.set_type(self.get(nm), i))

        return proxyip

    def parse(self, soup):
        result = []
        for d in soup.find('body').contents:
            try:
                d = str(d).strip()
                if d != '' and d[0].isdigit():
                    ip = {
                        "ip": d.split(':')[0],
                        "port": d.split(':')[1],
                        "info": "",
                        "type": 0,
                    }
                    result.append(ip)
            except Exception as e:
                logger.error('IP66API parse error: %s', e)

        return result

    def set_type(self, proxyip=[], iptype=0):
        result = []
        for ip in proxyip:
            ip['type'] = iptype
            result.append(ip)

        return result


class IP002(Base):
    """ http://www.ip002.com/free.html """

    def crawl(self):
        base = "http://www.ip002.com/free.html"
        proxyip = self.get(base, encoding="GBK")
        return proxyip

    def parse(self, soup):
        result = []
        s = soup.find("table").find_all("tr")
        for d in s:
            try:
                w = d.find_all("td")
                ip = {
                    "ip": w[0].string,
                    "port": w[1].string,
                    "info": w[3].string,
                    "type": 0,
                }
                if w[2].string == "透明":
                    ip['type'] = 1
                elif w[2].string == "高匿":
                    ip['type'] = 3

                result.append(ip)

            except Exception as e:
                logger.error('IP002 parse error: %s', e)

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
                    logger.error('CNProxy parse error: %s', e)

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
            ip["type"] = 1
        elif d[2].string == "匿名":
            ip["type"] = 2
        elif d[2].string == "高度匿名":
            ip["type"] = 3

        return ip

