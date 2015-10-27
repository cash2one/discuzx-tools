#!usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals, print_function

import logging
from common.logger import build_file_logs

level = logging.INFO  # logging.DEBUG

# 注意指定的目录要有权限
model_record_log = build_file_logs("model_record_log", level)
model_remote_log = build_file_logs("model_remote_log", level)
