#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from gethour import KuaiDaiLi2, XiCiDaiLi, CNProxy, IP66
from getday import KuaiDaiLi, CZ88, IP002
from validate import Validate

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def main():
    count = 0
    print "start to work..."
    while True:
        cronhour()
        if count % 6 == 0:
            cronday()
            count = 0

        validate()

        count += 1

        print "goto sleep...."
        time.sleep(3600)
        print "wake up..."


def cronhour():
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

def validate():
    validate = Validate()
    validate.reflesh()
    validate.ping()


if __name__ == "__main__":
    main()
