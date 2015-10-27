#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

from qiniu.auth import Auth
from qiniu import BucketManager

from conf.store_config import *

q = Auth(ACCESS_KEY, SECRET_KEY)
bucket_instance = BucketManager(q)


def stat(file_name, bucket=None):
    """获取文件信息.
    """

    if not bucket:
        bucket = BUCKET_DOMAIN

    ret, err = bucket_instance.stat(bucket, file_name)
    if err is not None:
        print('error: %s ' % err)
        return
    print(ret)


def copy(bucket, key, bucket_name, key2):
    """复制文件.
    """

    if not bucket:
        bucket = BUCKET_DOMAIN

    if not bucket_name:
        bucket_name = BUCKET_DOMAIN

    ret, err = bucket_instance.copy(bucket, key, bucket_name, key2)
    if err is not None:
        print('error: %s ' % err)
        return


def move(bucket, key, bucket_name, key2):
    """移动文件.
    """

    if not bucket:
        bucket = BUCKET_DOMAIN

    if not bucket_name:
        bucket_name = BUCKET_DOMAIN

    ret, err = bucket_instance.move(bucket, key, bucket_name, key2)
    if err is not None:
        print('error: %s ' % err)
        return


def delete(key, bucket=None):
    """删除文件.
    """

    if not bucket:
        bucket = BUCKET_DOMAIN

    ret, err = bucket_instance.delete(bucket, key)
    if err is not None:
        print('error: %s ' % err)
        return


if __name__ == '__main__':
    """模块测试.
    """
    pass
