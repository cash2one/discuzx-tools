#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

import os


def search_match_files(directory):
    """对指定的目录进行文件扫描.
    """

    for i in os.listdir(directory):
        sub_path = os.path.join(directory, i)
        if os.path.isdir(sub_path):
            search_match_files(sub_path)
        else:
            pass
            # TODO: 记录入数据库


def update_match_files():
    """对入库的文件定期扫描上传.
    """

    # 从数据库扫描出文件.

    # 上传已扫描出的文件.

    # 更新上传成功的数据.

    # 移除文件到其它目录.
    pass
