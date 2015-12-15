#!usr/bin/env python
# coding: utf-8

"""任务相关参数的配置.
"""

from __future__ import unicode_literals, print_function

import functools

import pymongo
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from autoloads import Models

is_echo = False
db_pool_recycle = 60

robot_environ = False  # local/server数据库连接, False: local; True: server.

if robot_environ:
    forum_conn = 'mysql+pymysql://operate:4F9dE8IWB8pf0f2927PfEb9b7@127.0.0.1/%s?charset=utf8'
    robot_conn = "mysql+pymysql://develop:f0f2927PfEb9b74F9dE8IWB8p@127.0.0.1/%s?charset=utf8"

    MYSQL_CONFIG = dict(
            host="127.0.0.1",
            port=3306,
            user="operate",
            password="4F9dE8IWB8pf0f2927PfEb9b7",
            charset="utf8",
    )
else:
    forum_conn = 'mysql+pymysql://operate:4F9dE8IWB8pf0f2927PfEb9b7@123.57.176.248/%s?charset=utf8mb4'
    robot_conn = "mysql+pymysql://develop:f0f2927PfEb9b74F9dE8IWB8p@123.57.176.248/%s?charset=utf8mb4"

    MYSQL_CONFIG = dict(
            host="123.57.176.248",
            port=3306,
            user="operate",
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

cache_host = "127.0.0.1"
# cache_host = "localhost"

cache_port = 27017
cache_database = "dz_gen_data"

cache_option = {
    'host': cache_host,
    'port': cache_port,
    'database': cache_database
}


def mongodb_init(host, port, database):
    """mongodb 初始化对象.

        :param host: 主机
        :param port: 端口
        :param database: 数据库
    """

    client = pymongo.MongoClient(host, port)
    # client = motor.MotorClient(host, port, max_pool_size=5)
    database = client[database]

    return database


# ===================以下为Redis选项===================

# redis配置项
REDIS_CONFIG = dict(
        redis_host="127.0.0.1",
        redis_port=6379)


# password="E8IWB8pf0PfE4F9df2927b9b7")


# ===================以下为从数据库到ORM的映射===================


def generate_models(mysql_config, databases_config, database_name, column_prefix='__'):
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
                     echo=is_echo,
                     pool_recycle=db_pool_recycle,
                     column_prefix=column_prefix,
                     schema=_database)
    return _models


MYSQL_DATABASES_TABLES = dict(
        discuzx=[
            "bbs_common_member", "bbs_common_member_status", "bbs_ucenter_members", "bbs_forum_thread",
            "bbs_forum_post", "bbs_forum_attachment", "bbs_forum_memberrecommend",
        ]
)

# 增加相关的分表
bbs_forum_attachment_list = ["bbs_forum_attachment_%d" % i for i in range(0, 10)]
MYSQL_DATABASES_TABLES["discuzx"].extend(bbs_forum_attachment_list)

generate_models = functools.partial(generate_models, MYSQL_CONFIG, MYSQL_DATABASES_TABLES)
generate_db_models = generate_models("discuzx")

if __name__ == "__main__":
    pass
