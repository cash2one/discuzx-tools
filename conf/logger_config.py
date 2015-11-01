#!usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals, print_function

import logging
from common.logger import build_file_logs

level = logging.INFO  # logging.DEBUG

# 注意指定的目录要有权限
model_record_log = build_file_logs("model_record.log", level)
model_remote_log = build_file_logs("model_remote.log", level)
faker_data_log = build_file_logs("faker_data_log.log", level)
redis_data_log = build_file_logs("redis_data_log.log", level)
gateway_debug_log = build_file_logs("gateway_debug_log")
