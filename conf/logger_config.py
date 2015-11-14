#!usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals, print_function

import logging
from common.logger import build_file_logs

level = logging.INFO  # logging.DEBUG

# 注意指定的目录要有权限
faker_data_log = build_file_logs("faker_data", level)
redis_data_log = build_file_logs("redis_data", level)

docker_data_log = build_file_logs("docker_data", level)
docker_upload_only = build_file_logs("docker_upload_only", level)

model_record_log = build_file_logs("model_record", level)
model_remote_log = build_file_logs("model_remote", level)

gateway_debug_log = build_file_logs("gateway_debug", level)
