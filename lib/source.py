#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author:  jiehua233@gmail.com
# @site:    http://chenjiehua.me
# @date:    2016-08-25
#

"""说明

代理IP匿名程度,：3=高匿；2=普匿；1=透明；0=未知
存储格式：（ip, port, anonymous)
"""

import sys
import logging
import requests
from bs4 import BeautifulSoup


reload(sys)
sys.setdefaultencoding("utf-8")


def request(url, encoding=None, headers=None):
    soup = None
    logging.info("Get contents from %s", url)
    try:
        r = requests.get(url, headers=headers) if headers else requests.get(url)
        if encoding:
            r.encoding = encoding

        if r.status_code == requests.codes.ok:
            soup = BeautifulSoup(r.text, "html5lib")
        else:
            logging.error("http response err, code: %s", r.status_code)
    except Exception as e:
        logging.error("requests get %s, err: %s", url, e)

    return soup


class CZ88:
    """ http://www.cz88.net/proxy/http_2.shtml """

    def get(self):
        base = "http://www.cz88.net/proxy/"
        ips = set()
        pages = ["index.shtml"] + ["http_%d.shtml" % i for i in range(2, 11)]
        for page in pages:
            soup = request(base + page, encoding="GBK")
            if soup:
                ips.update(self.crawl(soup))

        return ips

    def crawl(self, soup):
        result = set()
        soup = soup.find("div", id="boxright").find_all("li")
        for s in soup[1:]:
            try:
                v = [v for v in s.stripped_strings]
                ip = (v[0], v[1], 1)
                result.add(ip)
            except Exception as e:
                logging.error("CZ88 parse error: %s", e)

        return result


class KuaiDaili:
    """ www.kuaidaili.com """

    def get(self):
        base = "http://www.kuaidaili.com/"
        ips = set()
        for sub in ["proxylist", "free/inha", "free/intr", "free/outha", "free/outtr"]:
            for i in range(1, 11):
                soup = request(base + sub + "/%s" % i)
                if soup:
                    ips.update(self.crawl(soup))

        return ips

    def crawl(self, soup):
        result = set()
        for s in soup.find("table").find_all("tr")[1:]:
            try:
                d = s.find_all("td")
                if d[2].string == "透明":
                    anonymous = 1
                elif d[2].string == "匿名":
                    anonymous = 2
                elif d[2].string == "高匿名":
                    anonymous = 3
                else:
                    anonymous = 0
                ip = (d[0].string, d[1].string, anonymous)
                result.add(ip)

            except Exception as e:
                logging.error('KuaiDaili parse error: %s', e)

        return result


class XiciDaili:
    """ www.xicidaili.com"""

    def get(self):
        base = "http://www.xicidaili.com/"
        ips = set()
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36",
        }
        for u in ["nn", "nt", "wn", "wt"]:
            for i in range(1, 11):
                soup = request(base + u + "/%s" % i, headers=headers)
                if soup:
                    ips.update(self.crawl(soup))

        return ips

    def crawl(self, soup):
        result = set()
        for s in soup.find("table").find_all("tr")[1:]:
            try:
                d = s.find_all("td")
                if d[4].string == "透明":
                    anonymous = 1
                elif d[4].string == "匿名":
                    anonymous = 2
                elif d[4].string == "高匿":
                    anonymous = 3
                else:
                    anonymous = 0

                ip = (d[1].string, d[2].string, anonymous)
                result.add(ip)

            except Exception as e:
                logging.error("XiCiDaili parse error: %s", e)

        return result


class IP66:
    """ www.66ip.cn """

    def get(self):
        base = "http://www.66ip.cn/"
        base_ = [""] + ["areaindex_%s/" % i for i in range(1, 35)]
        ips = set()
        for b in base_:
            for i in range(1, 11):
                soup = request(base + b + "%s.html" % i, encoding="UTF-8")
                if soup:
                    ips.update(self.crawl(soup))

        return ips

    def crawl(self, soup):
        result = set()
        for s in soup.find_all("table")[2].find_all("tr")[1:]:
            try:
                d = s.find_all("td")
                if d[3].string == "透明":
                    anonymous = 1
                elif d[3].string == "匿名":
                    anonymous = 2
                elif d[3].string == "高匿代理":
                    anonymous = 3
                else:
                    anonymous = 0

                ip = (d[0].string, d[1].string, anonymous)
                result.add(ip)

            except Exception as e:
                logging.error('IP66 parse error: %s', e)

        return result


class IP66API:
    """ www.66ip.cn/nm.html """

    def get(self):
        ips = set()
        url = [
            # 普通代理
            ("http://www.66ip.cn/mo.php?tqsl=10000", 1),
            # 超级匿名
            ("http://www.66ip.cn/nmtq.php?getnum=10000&anonymoustype=4&proxytype=2&api=66ip", 3),
            # 透明，普匿，高匿
            ("http://www.66ip.cn/nmtq.php?getnum=10000&anonymoustype=3&proxytype=2&api=66ip", 3),
            ("http://www.66ip.cn/nmtq.php?getnum=10000&anonymoustype=2&proxytype=2&api=66ip", 2),
            ("http://www.66ip.cn/nmtq.php?getnum=10000&anonymoustype=1&proxytype=2&api=66ip", 1),
        ]
        for u in url:
            soup = request(u[0])
            if soup:
                ips.update(self.crawl(soup, u[1]))

        return ips

    def crawl(self, soup, anonymous=0):
        result = set()
        for d in soup.find('body').contents:
            try:
                d = str(d).strip()
                if d != "" and d[0].isdigit():
                    ip_, port_ = d.split(":")
                    ip = (ip_, port_, anonymous)
                    result.add(ip)
            except Exception as e:
                logging.error("IP66API parse error: %s", e)

        return result


class CNProxy:
    """ http://cn-proxy.com """

    def get(self):
        url = [
            ("http://cn-proxy.com", 3),
            ("http://cn-proxy.com/archives/218", 0),
        ]
        ips = set()
        for u in url:
            soup = request(u[0])
            if soup:
                ips.update(self.crawl(soup, u[1]))

        return ips

    def crawl(self, soup, anonymous=0):
        result = set()
        for s in soup.find_all("table"):
            for t in s.find_all("tr")[2:]:
                try:
                    d = t.find_all("td")
                    if not anonymous:
                        if d[2].string == "透明":
                            anonymous = 1
                        elif d[2].string == "匿名":
                            anonymous = 2
                        elif d[2].string == "高度匿名":
                            anonymous = 3

                    ip = (d[0].string, d[1].string, anonymous)
                    result.add(ip)

                except Exception as e:
                    logging.error("CNProxy parse error: %s", e)

        return result
