#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author   jiehua233@gmail.com
# @site     http://chenjiehua.me
# @date     2015-12-16
#

import logging

from etc.config import LOGGER

def get_logger():
    logger = logging.getLogger('ipproxy')
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        # logging format
        fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        # filehandler
        fh = logging.FileHandler(LOGGER['PATH'])
        fh.setFormatter(fmt)
        fh.setLevel(logging.DEBUG)
        logger.addHandler(fh)
        # streamhandler
        ch = logging.StreamHandler()
        ch.setFormatter(fmt)
        ch.setLevel(logging.INFO)
        logger.addHandler(ch)

    return logger


logger = get_logger()
