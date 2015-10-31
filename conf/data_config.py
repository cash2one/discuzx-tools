#!usr/bin/env python
# coding: utf-8

"""任务相关参数的配置.
"""

from __future__ import unicode_literals, print_function

import functools
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from autoloads import Models

is_echo = False
db_pool_recycle = 60

robot_environ = False  # local/server数据库连接, False: local; True: server.

if robot_environ:
    forum_conn = 'mysql+pymysql://develop:f0f2927PfEb9b74F9dE8IWB8p@127.0.0.1/%s?charset=utf8mb4'
    robot_conn = "mysql+pymysql://develop:f0f2927PfEb9b74F9dE8IWB8p@127.0.0.1/%s?charset=utf8mb4"

    MYSQL_CONFIG = dict(
        host="127.0.0.1",
        port=3306,
        user="develop",
        password="f0f2927PfEb9b74F9dE8IWB8p",
        charset="utf8",
    )
else:
    forum_conn = 'mysql+pymysql://develop:4F9dE8IWB8pf0f2927PfEb9b7@127.0.0.1/%s?charset=utf8mb4'
    robot_conn = "mysql+pymysql://develop:4F9dE8IWB8pf0f2927PfEb9b7@127.0.0.1/%s?charset=utf8mb4"

    MYSQL_CONFIG = dict(
        host="127.0.0.1",
        port=3306,
        user="develop",
        password="4F9dE8IWB8pf0f2927PfEb9b7",
        charset="utf8",
    )

forum_url = forum_conn % "discuzx"
robot_url = robot_conn % "roboter"

forum_engine = create_engine(forum_url, echo=is_echo, pool_recycle=db_pool_recycle)
robot_engine = create_engine(robot_url, echo=is_echo, pool_recycle=db_pool_recycle)

forum_session = scoped_session(sessionmaker(bind=forum_engine))()
robot_session = scoped_session(sessionmaker(bind=robot_engine))()
Base = declarative_base()

# ===================以下为CacheDB选项===================

# 是否启用Cache, False: 不启用; True: 启用
CACHE_DB_ON = True

cache_host = "localhost"
cache_port = 27017
cache_database = "dz_gen_data"

cache_option = {
    'host': cache_host,
    'port': cache_port,
    'database': cache_database
}


# ===================以下为从数据库到ORM的映射===================


def generate_models(mysql_config, databases_config, database_name, column_prefix='_'):
    """"从数据库表生成模型.

        mysql_config:        MySQL配置
        databases_config:    数据库配置
        database_name:　     数据库名称
        column_prefix:       属性(列)前缀
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
                     echo=is_echo,
                     pool_recycle=db_pool_recycle,
                     column_prefix=column_prefix,
                     schema=_database)
    return _models


MYSQL_DATABASES_TABLES = dict(
    discuzx=[
        "bbs_common_member", "bbs_forum_thread", "bbs_forum_post",
        "bbs_forum_attachment", "bbs_forum_attachment_0"
    ]
)

generate_models = functools.partial(generate_models, MYSQL_CONFIG, MYSQL_DATABASES_TABLES)
generate_db_models = generate_models("discuzx")
