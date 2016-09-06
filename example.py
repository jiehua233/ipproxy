#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author   jiehua233@gmail.com
# @site     http://chenjiehua.me
# @date     2016-09-06
#

"""proxy ip example

"""

import csv
import random
import requests

retrymax = 3
timeout = 30
proxycsv = "output.csv"
target = "http://www.baidu.com"


def main():
    total_weight, proxyip = load_proxyip(proxycsv)
    for i in range(retrymax):
        ip = get_proxyip(total_weight, proxyip)
        print "Using proxy:", ip
        try:
            r = requests.get(target, proxies={"http": "http://" + ip}, timeout=timeout)
            print "Http resp code:", r.status_code
            break

        except Exception as e:
            print e


def load_proxyip(fpath):
    """ proxyip list with weight
    """
    total_weight, proxyip = 0, []
    with open(fpath) as f:
        csvreader = csv.DictReader(f, restval=0, delimiter=",",
                                   quotechar="\"", quoting=csv.QUOTE_MINIMAL)
        for row in csvreader:
            ip = row["ip"] + ":" + row["port"]
            weight = 1/float(row["speed"])
            total_weight += weight
            proxyip.append((ip, weight))

    return total_weight, proxyip


def get_proxyip(total_weight, proxyip):
    r = random.uniform(0, total_weight)
    upto = 0
    for ip, weight in proxyip:
        if upto + weight >= r:
            return ip
        upto += weight

    print "Error: total_weight=%s, random_weight=%s" % (total_weight, r)
    return "localhost:8888"


if __name__ == "__main__":
    main()
