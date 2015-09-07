#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import urlparse
import json

from bs4 import BeautifulSoup
from base import Base

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

"""实时获取"""
class KuaiDaiLi2(Base):
    """www.kuaidaili.com

    """
    base = "http://www.kuaidaili.com/proxylist/"

    def do(self):
        self.get()
        self.redis.set("proxy_ip_kuaidaili2", json.dumps(self.ips))
        print len(self.ips)
        self.ping()

    def get(self):
        for i in range(1, 11):
            url = urlparse.urljoin(self.base, str(i))
            self._get(url)

    def _get(self, url):
        print "get: %s" % url
        r = requests.get(url)
        if r.status_code != requests.codes.ok:
            print "requests get error!"
            return

        soup = BeautifulSoup(r.text, "html.parser")
        for s in soup.find("table").find_all("tr")[1:]:
            try:
                d = s.find_all("td")
                ip = {
                    "ip": d[0].string,
                    "port": d[1].string,
                    "info": d[5].string,
                }
                if d[2].string == "透明":
                    ip["t"] = 1
                elif d[2].string == "匿名":
                    ip["t"] = 2
                elif d[2].string == "高匿名":
                    ip["t"] = 3
                else:
                    ip["t"] = 0

                self.ips.append(ip)

            except Exception, e:
                print e


class XiCiDaiLi(Base):
    """www.xicidaili.com

    """
    base = "http://www.xicidaili.com"

    def do(self):
        self.get()
        self.redis.set("proxy_ip_xicidaili", json.dumps(self.ips))
        print len(self.ips)
        self.ping()

    def get(self):
        for u in ["nn", "nt", "wn", "wt"]:
            url = urlparse.urljoin(self.base, u)
            self._get(url)

    def _get(self, url):
        print "get: %s" % url
        headers = {
            "Host": "www.xicidaili.com",
            "Referer": "http://www.xicidaili.com",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36",
        }
        r = requests.get(url, headers=headers)
        if r.status_code != requests.codes.ok:
            print "requests get error!"
            return

        soup = BeautifulSoup(r.text, "html.parser")
        for s in soup.find("table").find_all("tr")[1:]:
            try:
                d = s.find_all("td")
                ip = {
                    "ip": d[2].string,
                    "port": d[3].string,
                }
                info = d[4].find("a")
                if info:
                    ip["info"] = info.string

                if d[5].string == "透明":
                    ip["t"] = 1
                elif d[5].string == "匿名":
                    ip["t"] = 2
                elif d[5].string == "高匿":
                    ip["t"] = 3
                else:
                    ip["t"] = 0

                self.ips.append(ip)

            except Exception, e:
                print e


class CNProxy(Base):
    """cn-proxy.com

    """
    base = "http://cn-proxy.com"

    def do(self):
        self.get()
        self.redis.set("proxy_ip_cnproxy", json.dumps(self.ips))
        print len(self.ips)
        self.ping()

    def get(self):
        self._get(self.base, True)
        self._get(urlparse.urljoin(self.base, "archives/218"), False)

    def _get(self, url, flag):
        print "get: %s" % url
        r = requests.get(url)
        if r.status_code != requests.codes.ok:
            print "requests get error!"
            return

        soup = BeautifulSoup(r.text, "html.parser")
        for s in soup.find_all("table"):
            for t in s.find_all("tr")[2:]:
                try:
                    d = t.find_all("td")
                    ip = self._ip(d) if flag else self._ip2(d)
                    self.ips.append(ip)

                except Exception, e:
                    print e

    def _ip(self, d=[]):
        ip = {
            "ip": d[0].string,
            "port": d[1].string,
            "info": d[2].string,
            "t": 3,
        }
        return ip

    def _ip2(self, d=[]):
        ip = {
            "ip": d[0].string,
            "port": d[1].string,
            "info": d[3].string,
        }
        if d[2].string == "透明":
            ip["t"] = 1
        elif d[2].string == "匿名":
            ip["t"] = 2
        elif d[2].string == "高度匿名":
            ip["t"] = 3
        else:
            ip["t"] = 0

        return ip


class IP66(Base):
    """www.66ip.cn

    """
    base = "http://www.66ip.cn"

    def do(self):
        self.get()
        self.redis.set("proxy_ip_66ip", json.dumps(self.ips))
        print len(self.ips)
        self.ping()

    def get(self):
        for i in range(1, 11):
            url = urlparse.urljoin(self.base, "%s.html" % i)
            self._get(url)

    def _get(self, url):
        print "get: %s" % url
        r = requests.get(url)
        if r.status_code != requests.codes.ok:
            print "requests get error!"
            return

        soup = BeautifulSoup(r.text, "html.parser")
        for s in soup.find_all("table")[2].find_all("tr")[1:]:
            try:
                d = s.find_all("td")
                ip = {
                    "ip": d[0].string,
                    "port": d[1].string,
                    "info": d[2].string,
                }
                if d[3].string == "透明":
                    ip["t"] = 1
                elif d[3].string == "匿名":
                    ip["t"] = 2
                elif d[3].string == "高匿代理":
                    ip["t"] = 3
                else:
                    ip["t"] = 0

                self.ips.append(ip)

            except Exception, e:
                print e


