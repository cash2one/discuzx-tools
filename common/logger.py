#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""记录日志到文件.
"""

from __future__ import unicode_literals, print_function

import os
import logging

logs_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")


def build_file_logs(logger_name, level=logging.INFO):
    """创建文件日志.

        :parameter logger_name: 日志名称
        :parameter level
    """

    log_path = os.path.join(logs_path, "%s.log" % logger_name)
    if not os.path.exists(logs_path):
        os.makedirs(logs_path)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh = logging.FileHandler(log_path)
    fh.setFormatter(formatter)

    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    logger.addHandler(fh)

    return logger
