#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author:  jiehua233@gmail.com
# @sitef:   http://chenjiehua.me
# @date:    2016-09-05
#

import argparse
import multiprocessing
from validate import Validator

def main():
    args = parse_args()
    validator = Validator(args.target, args.timeout, args.process_num, args.thread_num)
    result = validator.run(args.input_csv)
    list(result)


def parse_args():
    procs_num = multiprocessing.cpu_count()
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv", help="the available proxy ip list, in csv format")
    parser.add_argument("--target", default="http://www.baidu.com", help="target uri to validate proxy ip, default: http://www.baidu.com")
    parser.add_argument("--timeout", type=int, default=30, help="timeout of validating each ip, default: 30s")
    parser.add_argument("--process_num", type=int, default=procs_num, help="run in multi process, default: CPU cores")
    parser.add_argument("--thread_num", type=int, default=100, help="run in multi thread of each process, default: 100")

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
