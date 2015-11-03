#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

import time
from urlparse import urljoin

from qiniu.io import PutExtra, put, put_file
from qiniu.auth import digest
from qiniu.rs import PutPolicy, GetPolicy, Client

from conf.store_config import BUCKET_DOMAIN, BUCKET_NAME, PUBLIC_BUCKET_DOMAIN, PUBLIC_BUCKET_NAME, UNIX_TIME_TTL

bucket_instance = Client()

try:
    from urllib.parse import urljoin
    from urllib.request import urlopen, Request
except ImportError:
    from urlparse import urljoin
    from urllib2 import urlopen, Request


def get_up_token():
    """生成上传凭证.
    """

    policy = PutPolicy(BUCKET_NAME)
    policy.expires = UNIX_TIME_TTL
    up_token = policy.token()

    return up_token


def put_up_datum(file_path, key, kind="file"):
    """上传资料, 三种模式: data, file, stream

        :parameter file_path
        :parameter key
        :parameter kind
    """

    token = get_up_token()
    if kind == "data":
        extra = PutExtra()
        extra.mime_type = "text/plain"
        ret, info = put(token, key, file_path,extra)
    else:
        ret, info = put_file(token, key, file_path)

    return ret, info


def get_dl_token(file_name, unix_time=None):
    """生成下载凭证.

        :param file_name: 文件名
        :param unix_time: 到期unix_time(时间戳)
    """

    # 如果传入时间戳小于一分钟
    if unix_time and int(unix_time) - int(time.time()) > UNIX_TIME_TTL - 60:
        unix_time = int(time.time()) + UNIX_TIME_TTL

    # 如果时间戳为空
    if not unix_time:
        unix_time = int(time.time()) + UNIX_TIME_TTL

    down_load_url = 'http://%s/%s?e=%s' % (BUCKET_DOMAIN, file_name, unix_time)
    dl_token = digest.Mac().sign(down_load_url)

    return dl_token, unix_time


def get_shift_rs_url(file_info, bucket=None):
    """生成带Token凭证的url地址.

        :parameter file_info: 文件名[?imageView2/1/w/200/h/200]
        :parameter bucket
    """

    if not bucket:
        bucket = BUCKET_DOMAIN

    base_url = 'http://%s/%s' % (bucket, file_info)

    policy = GetPolicy(expires=UNIX_TIME_TTL)
    private_url = policy.make_request(base_url)

    return private_url


def get_public_dl_url(file_name, suffix=None):
    """公共空间：下载地址.

        :parameter file_name
        :parameter suffix
    """

    if not file_name:
        raise ValueError
    if suffix:
        file_name += suffix

    base_url = PUBLIC_BUCKET_DOMAIN or 'http://%s.qiniudn.com/' % PUBLIC_BUCKET_NAME
    return urljoin(base_url, file_name)


def del_remote_dl_key(key, bucket=None):
    """删除文件.

        :parameter key
        :parameter bucket
    """

    if not bucket:
        bucket = BUCKET_DOMAIN

    ret, err = bucket_instance.delete(bucket, key)
    return err


if __name__ == '__main__':
    """单元测试.
    """
    pass
