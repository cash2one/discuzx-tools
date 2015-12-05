#!usr/bin/env python
# coding: utf-8

"""任务牵涉的数据模型.
"""

from __future__ import unicode_literals, print_function

import os
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
      `md5sum` VARCHAR(80) DEFAULT '' COMMENT '文件信息摘要Hash',
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
    md5sum = Column(VARCHAR, default='')
    plate = Column(INTEGER, default=0)
    status = Column(INTEGER, default=0)
    author = Column(VARCHAR, default='')
    create_datetime = Column(TIMESTAMP, nullable=False)
    upload_datetime = Column(TIMESTAMP, nullable=True)

    def __init__(self, file_name, key_name, plate=0, author='', md5sum=''):
        """扫描文件目录记录入库.
        """

        self.file_name = file_name
        self.key_name = key_name
        self.plate = plate
        self.author = author
        self.md5sum = md5sum
        self.create_datetime = datetime.datetime.now()

    def after_upload_action(self, down_link):
        """上传后更新.
        """

        self.down_link = down_link
        self.status = 1
        self.file_name = os.path.basename(self.file_name)
        self.upload_datetime = datetime.datetime.now()
        return self


class Surplus(BasicBase):
    """
    CREATE TABLE `bbs_surplus` (
      `id` INT NOT NULL AUTO_INCREMENT COMMENT '自动编号',
      `fid` INT DEFAULT 0 COMMENT '版块',
      `path` VARCHAR(255) NOT NULL COMMENT '文件名',
      `md5sum` VARCHAR(80) DEFAULT '' COMMENT '文件信息摘要Hash',
      `plate` INT DEFAULT 0 COMMENT '版块',
      `author` VARCHAR(45) DEFAULT '' COMMENT '所属用户',
      `create_datetime` timestamp NOT NULL COMMENT '记录时间',
      PRIMARY KEY (`id`)  COMMENT '文件重复日志');
    """
    __tablename__ = "bbs_surplus"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    fid = Column(INTEGER, default=0)
    path = Column(VARCHAR, nullable=False)
    md5sum = Column(VARCHAR, default='')
    plate = Column(INTEGER, default=0)
    author = Column(VARCHAR, default='')
    create_datetime = Column(TIMESTAMP, nullable=False)

    def __init__(self, file_name, plate=0, author='', md5sum='', fid=0):
        """重复文件记录日志.
        """

        self.fid = fid
        self.path = file_name
        self.plate = plate
        self.author = author
        self.md5sum = md5sum
        self.create_datetime = datetime.datetime.now()


class Member(BasicBase):
    """
    CREATE TABLE `bbs_member` (
      `id` INT NOT NULL AUTO_INCREMENT COMMENT '自动编号',
      `username` VARCHAR(45) NOT NULL COMMENT '账户名',
      `password` VARCHAR(45) NOT NULL COMMENT '账户密码',
      `email` VARCHAR(45) NOT NULL COMMENT '邮箱',
      `dz_uid` INT DEFAULT 0 COMMENT '论坛的uid',
      `create_datetime` timestamp NOT NULL COMMENT '添入时间',
      PRIMARY KEY (`id`)  COMMENT '自动注册用户');
    """

    __tablename__ = "bbs_member"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    username = Column(VARCHAR, nullable=False)
    password = Column(VARCHAR, nullable=False)
    email = Column(VARCHAR, default='')
    dz_uid = Column(INTEGER, default=0)
    create_datetime = Column(TIMESTAMP, nullable=False)

    def __init__(self, username, password, email, uid):
        """存放自动注册的账户信息.
        """

        self.username = username
        self.password = password
        self.email = email
        self.dz_uid = uid
        self.create_datetime = datetime.datetime.now()


class Thread(BasicBase):
    """
    CREATE TABLE `bbs_thread` (
      `id` INT NOT NULL AUTO_INCREMENT COMMENT '自动编号',
      `thread_id` INT NOT NULL COMMENT '主题ID',
      `post_id` INT NOT NULL COMMENT '帖子ID',
      `plate_id` INT NOT NULL COMMENT '版块ID',
      `attachment_id` INT DEFAULT 0 COMMENT '附件ID',
      `robot_data_id` INT DEFAULT 0 COMMENT '入库文件ID',
      `create_datetime` timestamp NOT NULL COMMENT '添入时间',
      PRIMARY KEY (`id`)  COMMENT '自动发文件帖子');
    """

    __tablename__ = "bbs_thread"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    thread_id = Column(INTEGER)
    post_id = Column(INTEGER)
    plate_id = Column(INTEGER)
    attachment_id = Column(INTEGER)
    robot_data_id = Column(INTEGER)
    create_datetime = Column(TIMESTAMP)

    def __init__(self, thread_id, post_id, plate_id, attachment_id=0, robot_data_id=0):
        """存放发帖信息.
        """

        self.thread_id = thread_id
        self.post_id = post_id
        self.plate_id = plate_id
        self.attachment_id = attachment_id
        self.robot_data_id = robot_data_id
        self.create_datetime = datetime.datetime.now()


class Post(BasicBase):
    """
    CREATE TABLE `bbs_post` (
      `id` INT NOT NULL AUTO_INCREMENT COMMENT '自动编号',
      `uid` INT NOT NULL DEFAULT 0 COMMENT 'Dz用户Id',
      `tid` VARCHAR(45) NOT NULL DEFAULT 0 COMMENT 'Dz主题Id',
      `pid` INT NOT NULL DEFAULT 0 COMMENT 'Dz帖子Id',
      `create_datetime` timestamp NOT NULL COMMENT '自动回帖时间',
      PRIMARY KEY (`id`) COMMENT '自动回帖');
    """

    __tablename__ = "bbs_post"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    uid = Column(INTEGER)
    tid = Column(INTEGER)
    pid = Column(INTEGER)
    create_datetime = Column(TIMESTAMP)

    def __init__(self, uid, tid, pid):
        """存放回帖信息.
        """

        self.uid = uid
        self.tid = tid
        self.pid = pid
        self.create_datetime = datetime.datetime.now()
