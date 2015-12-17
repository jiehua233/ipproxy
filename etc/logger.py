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
    logger.setLevel('DEBUG')
    if not logger.handlers:
        fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh = logging.FileHandler(LOGGER['PATH'])
        fh.setLevel('DEBUG')
        fh.setFormatter(fmt)
        logger.addHandler(fh)

    return logger


logger = get_logger()
