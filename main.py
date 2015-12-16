#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author   jiehua233@gmail.com
# @site     http://chenjiehua.me
# @date     2015-12-15
#

from crawler import Crawler
from crawler.hourly import IP002, IP66API


def main():
    ip66api = IP66API()
    proxyip = ip66api.crawl()
    for ip in proxyip:
        print ip['ip'], ip['port']

if __name__ == "__main__":
    main()
