#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

import os

from qiniu import Auth, BucketManager, put_data, put_file, put_stream
from qiniu.compat import is_py2, is_py3
from conf.store_config import *

q = Auth(ACCESS_KEY, SECRET_KEY)
bucket_instance = BucketManager(q)

if is_py2:
    import sys
    import StringIO
    from urlparse import urljoin

    reload(sys)
    sys.setdefaultencoding('utf8')
    StringIO = StringIO.StringIO
elif is_py3:
    import io
    from urllib.parse import urljoin

    StringIO = io.StringIO


def get_up_token(file_name):
    """生成上传凭证.

        :parameter file_name 文件名
    """

    up_token = q.upload_token(BUCKET_NAME, file_name)
    return up_token


def put_up_datum(file_path, key, kind="file", progress_handler=None):
    """上传资料, 三种模式: data, file, stream

        :parameter file_path
        :parameter key
        :parameter kind
    """

    up_token = get_up_token(key)
    if kind == "data":
        with open(file_path, 'rb') as input_stream:
            data = input_stream.read()
            ret, info = put_data(key=key,
                                 data=data,
                                 check_crc=True,
                                 up_token=up_token,
                                 mime_type="application/octet-stream",
                                 progress_handler=progress_handler)
    elif kind == "stream":
        size = os.stat(file_path).st_size
        with open(file_path, 'rb') as input_stream:
            ret, info = put_stream(key=key,
                                   up_token=up_token,
                                   input_stream=input_stream,
                                   data_size=size,
                                   progress_handler=progress_handler)
    else:
        ret, info = put_file(key=key,
                             up_token=up_token,
                             file_path=file_path,
                             progress_handler=progress_handler)

    return ret, info


def get_shift_rs_url(file_info, bucket=None):
    """生成带Token凭证的url地址.

        :parameter file_info 文件名[?imageView2/1/w/200/h/200]
        :parameter bucket
    """

    if not bucket:
        bucket = BUCKET_DOMAIN

    base_url = 'http://%s/%s' % (bucket, file_info)
    private_url = q.private_download_url(base_url, expires=UNIX_TIME_TTL)

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
