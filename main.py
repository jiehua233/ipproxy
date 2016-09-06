#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author:  jiehua233@gmail.com
# @sitef:   http://chenjiehua.me
# @date:    2016-09-05
#

import gzip
import csv
import logging
import argparse
import multiprocessing
from validate import Validator


def main():
    args = parse_args()
    set_loglevel(args.log)
    validator = Validator(args.target, args.timeout, args.process_num, args.thread_num)
    ip_all = [ip for ip in read_csv(args.input_csv)]
    logging.info("Load proxy ip, total: %s", len(ip_all))
    result = validator.run(ip_all)
    result = sorted(result, key=lambda x: x["speed"])
    write_csv(result, args.output)


def parse_args():
    procs_num = multiprocessing.cpu_count()
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv", help="the input proxy ip list, in csv format(supprot gz)")
    parser.add_argument("--output", default="output.csv", help="the output proxy ip list, default: output.csv")
    parser.add_argument("--target", default="http://www.baidu.com", help="target uri to validate proxy ip, default: http://www.baidu.com")
    parser.add_argument("--timeout", type=int, default=15, help="timeout of validating each ip, default: 15s")
    parser.add_argument("--process_num", type=int, default=procs_num, help="run in multi process, default: CPU cores")
    parser.add_argument("--thread_num", type=int, default=100, help="run in multi thread of each process, default: 100")
    parser.add_argument("--log", default="info", help="set loggin level, e.g. debug, info, warn, error; default: info")
    args = parser.parse_args()
    return args


def set_loglevel(loglvl):
    level = logging.INFO
    if loglvl == "debug":
        level = logging.DEBUG
    elif loglvl == "info":
        level = logging.INFO
    elif loglvl == "warn":
        level = logging.WARN
    elif loglvl == "error":
        level = logging.ERROR
    else:
        logging.error("Unknown logging level: %s", loglvl)

    logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=level)
    logging.info("Set log level: %s", loglvl)


def read_csv(fpath):
    o = gzip.open if fpath.endswith(".gz") else open
    with o(fpath) as f:
        csvreader = csv.DictReader(f, restval=0, delimiter=",",
                                   quotechar="\"", quoting=csv.QUOTE_MINIMAL)
        for row in csvreader:
            yield row


def write_csv(ip_avaliable, output):
    logging.info("Save to file, total proxy ip: %s", len(ip_avaliable))
    header = ["ip", "port", "anonymous", "info", "speed"]
    with open(output, "w") as fw:
        w = csv.DictWriter(fw, fieldnames=header, restval="",
                       extrasaction="ignore", delimiter=",",
                       quotechar="\"", quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        for ip in ip_avaliable:
            w.writerow(ip)


if __name__ == "__main__":
    main()
