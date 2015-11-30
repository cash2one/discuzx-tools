#!usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals, print_function

import logging

from common.logger import build_file_logs

level = logging.INFO  # logging.DEBUG

# 注意指定的目录要有权限
redis_data_log = build_file_logs("redis_data", level)

model_record_log = build_file_logs("model_record", level)
model_remote_log = build_file_logs("model_remote", level)

record_info = build_file_logs("record_info", level)
upload_info = build_file_logs("upload_info", level)
upload_error = build_file_logs("upload_error", level)

post_info = build_file_logs("post_info", level)
user_info = build_file_logs("user_info", level)
recommend_info = build_file_logs("recommend_info", level)

gateway_debug_log = build_file_logs("gateway_debug", level)
