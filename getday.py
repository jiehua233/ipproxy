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

"""每日获取"""
class CZ88(Base):
    """ http://www.cz88.net/proxy/http_2.shtml

    """
    base = "http://www.cz88.net/proxy/"

    def do(self):
        self.get()
        self.redis.set("proxy_ip_cz88", json.dumps(self.ips))
        print len(self.ips)
        self.ping()

    def get(self):
        self._get("index.shtml")
        for i in range(2, 11):
            try:
                self._get("http_%d.shtml" % i)
            except Exception, e:
                print e

    def _get(self, page):
        url = urlparse.urljoin(self.base, page)
        print "get: %s" % url
        r = requests.get(url)
        r.encoding = "GBK"
        if r.status_code != requests.codes.ok:
            print "requests get error!"
            return

        soup = BeautifulSoup(r.text, "html.parser")
        soup = soup.find("div", id="boxright").find_all("li")
        keys = ["ip", "port", "t", "info"]
        for s in soup[1:]:
            try:
                ip = {}
                i = 0
                for d in s.stripped_strings:
                    ip[keys[i]] = d
                    i += 1
                ip["t"] = 1

                self.ips.append(ip)

            except Exception, e:
                print e


class KuaiDaiLi(Base):
    """ http://blog.kuaidaili.com/

    """
    base = "http://blog.kuaidaili.com/"

    def do(self):
        self.get()
        self.redis.set("proxy_ip_kuaidaili", json.dumps(self.ips))
        print len(self.ips)
        self.ping()

    def get(self):
        r = requests.get(self.base)
        if r.status_code  == requests.codes.ok:
            soup = BeautifulSoup(r.text, "html.parser")
            for s in soup.find_all("article")[:2]:
                url = s.find("a")["href"]
                print url
                try:
                    self._get(url)
                except Exception, e:
                    print e

    def _get(self, url):
        r = requests.get(url)
        if r.status_code != requests.codes.ok:
            print "requests get error!"
            return

        soup = BeautifulSoup(r.text, "html.parser")
        kwargs = {"class": "entry-content"}
        s = soup.find("div", **kwargs).find_all("p")
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
                    ip["t"] = 1
                elif rst[1] == "匿名":
                    ip["t"] = 2
                elif rst[1] == "高匿名":
                    ip["t"] = 3
                else:
                    ip["t"] = 0

                self.ips.append(ip)

            except Exception, e:
                print e


class IP002(Base):
    """http://www.ip002.com/

    """
    base = "http://www.ip002.com/"

    def do(self):
        self.get()
        self.redis.set("proxy_ip_ip002", json.dumps(self.ips))
        print len(self.ips)
        self.ping()

    def get(self):
        r = requests.get(self.base)
        if r.status_code == requests.codes.ok:
            soup = BeautifulSoup(r.text, "html.parser")
            kwargs = {"class": "post-title"}
            for s in soup.find_all("h2", **kwargs)[:2]:
                url = s.find("a")["href"]
                print url
                self._get(url)

    def _get(self, url):
        r = requests.get(url)
        if r.status_code != requests.codes.ok:
            print "requests get error!"
            return

        soup = BeautifulSoup(r.text, "html.parser")
        kwargs = {"class": "post-body"}
        s = soup.find("section", **kwargs).find_all("p")
        for d in s:
            try:
                i = d.string.split("#")
                ip = {
                    "ip": i[0].split(":")[0],
                    "port": i[0].split(":")[1],
                    "info": i[1],
                    "t": 0,
                }
                self.ips.append(ip)

            except Exception, e:
                print e
