#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author   jiehua233@gmail.com
# @site     http://chenjiehua.me
# @date     2015-12-15
#

from crawler import Crawler
from sniffer import Sniffer
from etc.logger import logger


def main():
    proxyips = Crawler.run()
    logger.info('Crawler finish, total ip: %s', len(proxyips))
    sniffer = Sniffer()
    sniffer.run(proxyips)

if __name__ == "__main__":
    main()
