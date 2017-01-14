#!usr/bin/env python
# coding: utf-8

import os

# 七牛设置
access_key = os.getenv('seven_access_key')
secret_key = os.getenv('seven_secret_key')
bucket_name = os.getenv('seven_bucket_name')
bucket_domain = os.getenv('seven_bucket_domain')

# MySQL设置
mysql_host = os.getenv('mysql_host')
mysql_port = os.getenv('mysql_port')
mysql_user = os.getenv('mysql_user')
mysql_password = os.getenv('mysql_password')
mysql_charset = os.getenv('mysql_charset')

robots_db = os.getenv('robots_schema')
discus_db = os.getenv('discus_schema')
discus_prefix = os.getenv('discus_prefix')

# Redis设置
redis_host = os.getenv('redis_host')
redis_port = os.getenv('redis_port')
redis_password = os.getenv('redis_password')

# mongodb设置
cache_host = os.getenv('cache_host')
cache_port = os.getenv('cache_port')
cache_user = os.getenv('cache_user')
cache_password = os.getenv('cache_password')
cache_database = os.getenv('cache_database')

# 站点百度Push设置
dz_site = os.getenv('dz_site')
dz_push_token = os.getenv('dz_push_token')

discuss_username = os.getenv('discuss_username', '')
discuss_password = os.getenv('discuss_password', '')

if __name__ == '__main__':
    print(locals())
