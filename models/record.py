#!usr/bin/env python
# coding: utf-8

"""任务牵涉的数据模型.
"""

from __future__ import unicode_literals, print_function

import datetime
from sqlalchemy import Column, INTEGER, VARCHAR, TIMESTAMP
from models.base import BasicBase


class Attachment(BasicBase):
    """
    CREATE TABLE `bbs_attachment` (
      `id` INT NOT NULL AUTO_INCREMENT COMMENT '自动编号',
      `file_name` VARCHAR(255) NOT NULL COMMENT '文件名',
      `key_name` VARCHAR(80) DEFAULT '' COMMENT '七牛文件名',
      `down_link` VARCHAR(150) DEFAULT '' COMMENT '下载地址',
      `plate` INT DEFAULT 0 COMMENT '版块',
      `status` INT DEFAULT 0 COMMENT '是否发帖(0:未传;1:已传;2:已发)',
      `author` VARCHAR(45) DEFAULT '' COMMENT '所属用户',
      `create_datetime` timestamp NOT NULL COMMENT '添入时间',
      `upload_datetime` timestamp NULL COMMENT '上传时间',
      PRIMARY KEY (`id`)  COMMENT '自动上传七牛文件');
    """

    __tablename__ = "bbs_attachment"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    file_name = Column(VARCHAR, nullable=False)
    key_name = Column(VARCHAR, default='')
    down_link = Column(VARCHAR, default='')
    plate = Column(INTEGER, default=0)
    status = Column(INTEGER, default=0)
    author = Column(VARCHAR, default='')
    create_datetime = Column(TIMESTAMP, nullable=False)
    upload_datetime = Column(TIMESTAMP, nullable=True)

    def __init__(self, file_name, plate=0, author=''):
        """扫描文件目录记录入库.
        """

        self.file_name = file_name
        self.plate = plate
        self.author = author
        self.create_datetime = datetime.datetime.now()

    def after_upload_action(self, key_name, down_link):
        """上传后更新.
        """

        self.key_name = key_name
        self.down_link = down_link
        self.status = 1
        self.upload_datetime = datetime.datetime.now()


class Member(BasicBase):
    """
    CREATE TABLE `bbs_member` (
      `id` INT NOT NULL AUTO_INCREMENT COMMENT '自动编号',
      `username` VARCHAR(45) NOT NULL COMMENT '账户名',
      `password` VARCHAR(45) NOT NULL COMMENT '账户密码',
      `email` VARCHAR(45) NOT NULL COMMENT '邮箱',
      `create_datetime` timestamp NOT NULL COMMENT '添入时间',
      PRIMARY KEY (`id`)  COMMENT '自动注册用户');
    """

    __tablename__ = "bbs_member"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    username = Column(VARCHAR)
    password = Column(VARCHAR)
    email = Column(VARCHAR)
    create_datetime = Column(TIMESTAMP)


class Thread(BasicBase):
    """
    CREATE TABLE `bbs_thread` (
      `id` INT NOT NULL AUTO_INCREMENT COMMENT '自动编号',
      `thread_id` INT NOT NULL COMMENT '帖子ID',
      `attachment_id` INT NOT NULL COMMENT '七牛文件ID',
      `create_datetime` timestamp NOT NULL COMMENT '添入时间',
      PRIMARY KEY (`id`)  COMMENT '自动发文件帖子');
    """

    __tablename__ = "forum_thread"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    thread_id = Column(INTEGER)
    attachment_id = Column(INTEGER)
    create_datetime = Column(TIMESTAMP)
