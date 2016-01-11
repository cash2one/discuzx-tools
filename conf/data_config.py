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

from conf.env_conf import mysql_host, mysql_port, mysql_user, mysql_password, mysql_charset

is_echo = False
db_pool_recycle = 60

robot_environ = False  # local/server数据库连接, False: local; True: server.
conn = 'mysql+pymysql://%(user)s:%(password)s@%(host)s:%(port)s/%(database)s?charset=%(charset)s'

if robot_environ:
    MYSQL_CONFIG = dict(
            host="127.0.0.1",
            port=3306,
            user="operate",
            password="4F9dE8IWB8pf0f2927PfEb9b7",
            charset="utf8")
else:
    MYSQL_CONFIG = dict(
            host=mysql_host if mysql_host else "123.57.176.248",
            port=mysql_port if mysql_port else 3306,
            user=mysql_user if mysql_user else "operate",
            password=mysql_password if mysql_password else "4F9dE8IWB8pf0f2927PfEb9b7",
            charset=mysql_charset if mysql_charset else "utf8")

MYSQL_CONFIG_NEW = MYSQL_CONFIG.copy()

MYSQL_CONFIG_NEW.update(database="discuzx")
forum_url = conn % MYSQL_CONFIG_NEW
MYSQL_CONFIG_NEW.update(database="roboter")
robot_url = conn % MYSQL_CONFIG_NEW

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

cache_port = 27027
cache_user = "wuuuang",
cache_password = "WJGFd9E6IWBWpf0f7HzEb2929b7",
cache_database = "dz_gen_data"

cache_option = {
    'host': cache_host,
    'port': cache_port,
    'database': cache_database,
    'username': cache_user,
    'password': cache_password,
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
        connection_string = "mongodb://%s:%s@%s:%d/%s" % (username, password, host, port, database)
        client = pymongo.MongoClient(connection_string)
    else:
        client = pymongo.MongoClient(host, port)
        # client = motor.MotorClient(host, port, max_pool_size=5)
    database = client[database]

    return database


# ===================以下为Redis选项===================

# redis配置项
REDIS_CONFIG = dict(
        redis_host="127.0.0.1",
        redis_port=6389,
        password="E8IWB8pf0PfE4F9df2927b9b7",
)


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
