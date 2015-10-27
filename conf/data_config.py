#!usr/bin/env python
# coding: utf-8

"""任务相关参数的配置.
"""

from __future__ import unicode_literals, print_function

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

is_echo = False
db_pool_recycle = 60

robot_environ = False  # local/server数据库连接, False: local; True: server.

if robot_environ:
    forum_conn = 'mysql+pymysql://develop:f0f2927PfEb9b74F9dE8IWB8p@127.0.0.1/%s?charset=utf8mb4'
    robot_conn = "mysql+pymysql://develop:f0f2927PfEb9b74F9dE8IWB8p@127.0.0.1/%s?charset=utf8mb4"
else:
    forum_conn = 'mysql+pymysql://develop:4F9dE8IWB8pf0f2927PfEb9b7@127.0.0.1/%s?charset=utf8mb4'
    robot_conn = "mysql+pymysql://develop:4F9dE8IWB8pf0f2927PfEb9b7@127.0.0.1/%s?charset=utf8mb4"

forum_url = forum_conn % "discuzx"
robot_url = robot_conn % "roboter"

forum_engine = create_engine(forum_url, echo=is_echo, pool_recycle=db_pool_recycle)
robot_engine = create_engine(robot_url, echo=is_echo, pool_recycle=db_pool_recycle)

forum_session = scoped_session(sessionmaker(bind=forum_engine))()
robot_session = scoped_session(sessionmaker(bind=robot_engine))()
Base = declarative_base()
