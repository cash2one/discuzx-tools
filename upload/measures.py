#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

from qiniu.rs import Client
from conf.store_config import BUCKET_DOMAIN

bucket_instance = Client()


def stat(file_name, bucket=None):
    """获取文件信息.

        :parameter file_name
        :parameter bucket
    """

    if not bucket:
        bucket = BUCKET_DOMAIN

    ret, err = bucket_instance.stat(bucket, file_name)
    if err is not None:
        print('error: %s ' % err)
        return


def copy(bucket, key, bucket_name, key2):
    """复制文件.

        :parameter bucket
        :parameter key
        :parameter bucket_name
        :parameter key2
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

        :parameter bucket
        :parameter key
        :parameter bucket_name
        :parameter key2
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

        :parameter bucket
        :parameter key
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
