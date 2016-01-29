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

discuss_username = os.getenv('discuss_username', '')
discuss_password = os.getenv('discuss_password', '')
