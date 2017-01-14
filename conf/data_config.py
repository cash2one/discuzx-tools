#!usr/bin/env python
# coding: utf-8

"""任务相关参数的配置.
"""

from __future__ import unicode_literals, print_function

import functools

import pymongo
from autoloads import Models
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from conf.env_conf import (
    mysql_host, mysql_port, mysql_user, mysql_password, mysql_charset,
    robots_db, discus_db, discus_prefix, redis_host, redis_port,
    redis_password, cache_host, cache_port, cache_user, cache_password,
    cache_database)

echo = False
pool_recycle = 60

conn = ('mysql+pymysql://%(user)s:%(password)s@'
        '%(host)s:%(port)s/%(database)s?charset=%(charset)s')

MYSQL_CONFIG = dict(
    host=mysql_host or '127.0.0.1',
    port=mysql_port or 3306,
    user=mysql_user,
    password=mysql_password,
    charset=mysql_charset or "utf8")

MYSQL_CONFIG.update(database=discus_db)
forum_url = conn % MYSQL_CONFIG

MYSQL_CONFIG.update(database=robots_db)
robot_url = conn % MYSQL_CONFIG

forum_engine = create_engine(forum_url, echo=echo, pool_recycle=pool_recycle)
robot_engine = create_engine(robot_url, echo=echo, pool_recycle=pool_recycle)

forum_session = scoped_session(sessionmaker(bind=forum_engine))()
robot_session = scoped_session(sessionmaker(bind=robot_engine))()
Base = declarative_base()

# ===================以下为CacheDB选项===================

# 是否启用Cache, False: 不启用; True: 启用
CACHE_DB_ON = True

cache_host = cache_host  # cache_host = "localhost"
cache_port = cache_port or 27027
cache_user = cache_user,
cache_password = cache_password,
cache_database = cache_database or "dz_gen_data"

if cache_user and cache_password:
    cache_host = "mongodb://%s:%s@%s:%s" % (
        cache_user, cache_password, cache_host, cache_port)

cache_option = {
    'host': cache_host,
    'port': cache_port,
    'database': cache_database,
}


def mongodb_init(host, port, database, username=None, password=None):
    """mongodb 初始化对象.

        :param host: 主机
        :param port: 端口
        :param database: 数据库
        :param username: 账户
        :param password: 密码
    """
    if username and password:
        connection_string = "mongodb://%s:%s@%s:%d/%s" % (
            username, password, host, port, database)
        client = pymongo.MongoClient(connection_string)
    else:
        client = pymongo.MongoClient(host, port)
        # client = motor.MotorClient(host, port, max_pool_size=5)
    database = client[database]

    return database


# ===================以下为Redis选项===================

# redis配置项
REDIS_CONFIG = dict(
    redis_host=redis_host,
    redis_port=redis_port or 6389,
    password=redis_password,
)


# ===================以下为从数据库到ORM的映射===================


def generate_models(mysql_config, databases_config, database_name,
                    column_prefix='__'):
    """"从数据库表生成模型.

        :parameter mysql_config:        MySQL配置
        :parameter databases_config:    数据库配置
        :parameter database_name:　     数据库名称
        :parameter column_prefix:       属性(列)前缀
    """

    _host = mysql_config['host']
    _port = mysql_config['port']
    _user = mysql_config['user']
    _password = mysql_config['password']
    _charset = mysql_config['charset']
    _database = database_name
    _tables = databases_config[_database]

    _models = Models(host=_host,
                     port=_port,
                     user=_user,
                     passwd=_password,
                     database=_database,
                     tables=_tables,
                     charset=_charset,
                     echo=echo,
                     pool_recycle=pool_recycle,
                     column_prefix=column_prefix,
                     schema=_database)
    return _models


MYSQL_DATABASES_TABLES = {
    discus_db: [
        "common_member", "common_member_status", "ucenter_members",
        "forum_thread",
        "forum_post", "forum_attachment", "forum_memberrecommend",
    ]
}

MYSQL_DATABASES_TABLES[discus_db] = [
    "%s_%s" % ('iky', i) for i in MYSQL_DATABASES_TABLES[discus_db]]

# 增加相关的分表
forum_attachment_list = [
    "%s_forum_attachment_%d" % (discus_prefix, i) for i in range(0, 10)]

MYSQL_DATABASES_TABLES[discus_db].extend(forum_attachment_list)

generate_models = functools.partial(
    generate_models, MYSQL_CONFIG, MYSQL_DATABASES_TABLES)

generate_db_models = generate_models(discus_db)
