#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conf.env_conf import access_key, secret_key, bucket_name, bucket_domain

# 默认100分钟
UNIX_TIME_TTL = 6000

ACCESS_KEY = access_key if access_key else 'NI_DlIj_otOCunan5oSCa5eG3HGIl3qK0pqtoNuI'
SECRET_KEY = secret_key if secret_key else '1yFjoq3HiB3v_n7wGzHBs20p6opiURrE5go1ksyB'

# 默认私有空间
BUCKET_NAME = bucket_name if bucket_name else "roboter"
BUCKET_DOMAIN = bucket_domain if bucket_domain else "source.ikuanyu.com"  # "7xo804.com1.z0.glb.clouddn.com"

# 默认公共空间
PUBLIC_BUCKET_NAME = ""
PUBLIC_BUCKET_DOMAIN = ""
