#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author:  jiehua233@gmail.com
# @site:    https://chenjiehua.me
# @date:    2016-08-25
#

import sys
import logging
import os.path
import IP
from lib.source import CZ88, KuaiDaili, XiciDaili, IP66, IP66API, CNProxy

reload(sys)
sys.setdefaultencoding("utf-8")
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
root = os.path.dirname(os.path.abspath(__file__))


def main():
    ip_pool = get_proxyip()
    sort_ip = sort_proxyip(ip_pool)
    save2csv(sort_ip)


def get_proxyip():
    ip_pool = set()
    for s in [CZ88, KuaiDaili, XiciDaili, IP66, IP66API, CNProxy]:
        instance = s()
        ips = instance.get()
        ip_pool.update(ips)
        logging.info("Totally got proxy ip: %s of %s", len(ips), len(ip_pool))

    return ip_pool


def sort_proxyip(pool):
    result = {
        "all": set(),
        "china": set(),
        "foreign": set(),
        "high_anonymous": set(),
        "low_anonymous": set(),
        "non_anonymous": set(),
    }
    for ip in pool:
        # country
        info = IP.find(ip[0]).strip().replace("\t", "-")
        ip_ = ip + (info,)
        result["all"].add(ip_)
        if info.startswith("中国"):
            result["china"].add(ip_)
        else:
            result["foreign"].add(ip_)

        # anonymous
        if ip[2] == 3:
            result["high_anonymous"].add(ip_)
        elif ip[2] == 2:
            result["low_anonymous"].add(ip_)
        else:
            result["non_anonymous"].add(ip_)

    return result


def save2csv(sort_ip):
    _dir = os.path.join(root, "data")
    if not os.path.exists(_dir):
        os.makedirs(_dir)

    for tag in sort_ip:
        output = os.path.join(_dir, "%s.csv" % tag)
        with open(output, "w") as fw:
            fw.write("ip,port,anonymous,info\n")
            for ip in sort_ip[tag]:
                fw.write("%s,%s,%s,%s\n" % ip)


if __name__ == "__main__":
    main()
