#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author   jiehua233@gmail.com
# @site     http://chenjiehua.me
# @date     2015-12-16
#

import time
import logging
import multiprocessing
import requests
import gevent
from gevent import monkey; monkey.patch_all()
from etc.config import SNIFFER

class Validator:

    def __init__(self):
        self.target = SNIFFER['TARGET']
        self.timeout = SNIFFER['TIMEOUT']
        self.process_num = SNIFFER['process_num']
        self.thread_num = SNIFFER['THREAD_NUM']

    def run_in_multiprocess(self, proxy_list):
        result_queue = multiprocessing.Queue()
        proxy_partitions = self.partite_proxy(proxy_list)
        process = []
        for partition in proxy_partitions:
            p = multiprocessing.Process(target=self.process_with_gevent, args=(result_queue, partition))
            p.start()
            process.append(p)

        for p in process:
            p.join()

        result = {}
        for p in process:
            result.update(result_queue.get())

        return result

    def partite_proxy(self, proxy_list):
        result = []
        step = len(proxy_list) / self.process_num
        for i in range(0, len(proxy_list), step):
            result.append(proxy_list[i:i+step])

        return result

    def process_with_gevent(self, result_queue, proxy_list):
        jobs = [gevent.spawn(self.validate_job, proxy_list) for i in range(self.thread_num)]
        gevent.joinall(jobs)
        result = {}
        for job in jobs:
            result.update(job.value)

        result_queue.put(result)

    def validate_job(self, proxy_list):
        result = {}
        while len(proxy_list) > 0:
            ip_port = proxy_list.pop()
            is_valid, speed = self.validate(ip_port)
            if is_valid:
                result[ip_port] = speed

        return result

    def validate(self, ip_port):
        logging.info("ping: %s" % ip_port)
        proxies = {
            "http": "http://%s" % ip_port,
        }
        try:
            start = time.time()
            r = requests.get(self.target, proxies=proxies, timeout=self.timeout)
            if r.status_code == requests.codes.ok:
                return True, time.time() - start

        except Exception as e:
            logging(e)

        return False, 0





    def ping(self):
        # 优先处理高匿名代理
        for i in self.r:
            skey = "proxy_ip_%s" % i
            zkey = "proxy_ip_ping_%s" % i
            ips = self.redis.smembers(skey)
            print skey, len(ips)
            for ip in ips:
                try:
                    start = time.time()
                    if self._ping(ip):
                        duration = time.time() - start
                        self.redis.zadd(zkey, duration, ip)
                        print "add to sorted set"
                    else:
                        self.redis.srem(skey, ip)
                        print "del from set"

                except Exception, e:
                    print e

