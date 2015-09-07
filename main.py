#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from gethour import KuaiDaiLi2, XiCiDaiLi, CNProxy, IP66
from getday import KuaiDaiLi, CZ88, IP002
from reflesh import Reflesh

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def main():
    count = 0
    print "start to work..."
    while True:
        start = time.time()
        cronhour()
        last = time.time()
        print "get hour: %s " % (last - start)

        if count % 6 == 0:
            cronday()
            print "get hour: %s " % (time.time() - last)
            count = 0

        count += 1
        print "goto sleep...."
        time.sleep(3600)
        print "wake up..."


def cronhour():
    # 刷新数据
    reflesh = Reflesh()
    reflesh.do()
    # 更新数据
    cnproxy = CNProxy()
    cnproxy.do()
    ip66 = IP66()
    ip66.do()
    xicidaili = XiCiDaiLi()
    xicidaili.do()
    kuaidaili2 = KuaiDaiLi2()
    kuaidaili2.do()

def cronday():
    cz88 = CZ88()
    cz88.do()
    kuaidaili = KuaiDaiLi()
    kuaidaili.do()
    ip002 = IP002()
    ip002.do()


if __name__ == "__main__":
    main()
