#!usr/bin/env python
# coding: utf-8

"""定义规则配置.
"""

from __future__ import unicode_literals, print_function

from libs.common.func import Utils
from envcfg.json.service import SEEK_DIR_CONF, USER_MAP_CONF, PLATE_MAP_CONF

# 计划跳过的文件列表
IGNORE_FILE_LIST = ["readme.txt", "README"]

# 是否要跳过列表文件
SKIP_README_FILE = True

# 是否启用规定的文件夹结构(版块/作者)
ENABLE_FOLDER_RULE = True

# 搜索目录
SEEK_DIRECTORY = SEEK_DIR_CONF

# 每次扫描数据数量
MATCH_FILES_LIMIT = 5

# 每次扫描时间间隔, 默认五分钟.
MATCH_FILES_INTERVAL = 1 * 60

# 用户映射配置
USER_MAP_CONFIG = USER_MAP_CONF

# 版块映射配置
PLATE_MAP_CONFIG = Utils.get_plate_map_conf(PLATE_MAP_CONF)
