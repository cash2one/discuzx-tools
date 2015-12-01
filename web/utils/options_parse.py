#!usr/bin/env python
# coding: utf-8

import os

from tornado.options import define, options
from tornado.log import app_log

define("port",
       type=int,
       help="系统监听端口！")

define("debug",
       default=False,
       type=bool,
       help="系统调试模式！")

define("config",
       default="web_config.conf",
       type=str,
       help="系统配置文件！")


def parse_options_config(path):
    """从配置文件读取配置参数.

        :parameter path: 配置文件目录
    """

    options.parse_command_line()
    if options.config:
        machine = os.getenv("service_host")
        if machine:
            options.config = "%s.%s" % (options.config, machine)
        app_log.info("初始化配置文件：%s" % options.config)
        options.parse_config_file(os.path.join(path, 'web_config.conf'))
