#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

import os
import uuid
import itertools

from twisted.internet import task
from twisted.internet import reactor

from conf.data_config import robot_session, REDIS_CONFIG
from conf.regular_config import SEEK_DIRECTORY, DONE_DIRECTORY, IGNORE_FILE_LIST, SKIP_README_FILE, \
    ENABLE_FOLDER_RULE, MATCH_FILES_LIMIT, MATCH_FILES_INTERVAL, USER_MAP_CONFIG, PLATE_MAP_CONFIG

from common.func import FileFinished, Utils, RedisService
from models.record import Attachment, Surplus
from upload import put_up_datum

fileFinished = FileFinished(SEEK_DIRECTORY, DONE_DIRECTORY)
redis_service = RedisService(db="files_md5sum", password=REDIS_CONFIG.get("password"))


def init_redis_data():
    """初始化redis的数据.
    """

    attachment_entities = robot_session.query(Attachment, Attachment.id, Attachment.md5sum).all()
    for entity in attachment_entities:
        redis_service.set(entity.md5sum, entity.id)


def search_match_files(directory):
    """对指定的目录文件扫描, 并结果入库.

        :parameter directory 指定的扫描目录
    """

    # 扫描文件
    for i in os.listdir(directory):
        sub_path = os.path.join(directory, i)
        if os.path.isdir(sub_path):

            # 跳过未适配的版块和作者.
            if ENABLE_FOLDER_RULE:
                base_name = os.path.basename(sub_path).lower()
                if base_name not in itertools.chain(PLATE_MAP_CONFIG.keys(), USER_MAP_CONFIG.keys()):
                    continue

            search_match_files(sub_path)
        else:

            # 跳过计划的文件列表.
            if SKIP_README_FILE:
                ignore_file_list = map(lambda x: x.lower(), IGNORE_FILE_LIST)
                if ignore_file_list and os.path.basename(sub_path).lower() in ignore_file_list:
                    continue

            # 版块与作者(plate=0, author='')的对应.
            if ENABLE_FOLDER_RULE:
                plate, author = Utils.get_info_by_path(sub_path)[:2]
                plate = PLATE_MAP_CONFIG.get(plate)
            else:
                plate, author = 0, ''

            # 如有重复记录到日志.
            md5sum = Utils.md5sum(sub_path)
            fid = redis_service.get(md5sum)
            if fid:
                Surplus(sub_path, plate=plate, author=author, md5sum=md5sum, fid=fid).save(robot_session)
                continue

            entity = Attachment(sub_path, plate=plate, author=author, md5sum=md5sum)
            entity.save(robot_session)
            redis_service.set(entity.md5sum, entity.id)


def upload_match_files(limit=5):
    """对结果入库的数据扫描, 并文件上传.

        :parameter limit: 检索数据数量
    """

    success_entities = []
    attachment_entities = robot_session.query(Attachment).filter(
        Attachment.status == 0).order_by(Attachment.id).limit(limit).all()

    if attachment_entities:
        for attachment in attachment_entities:
            suffix = Utils.get_info_by_path(attachment.file_name)[2]
            key_name = ''.join((uuid.uuid4().get_hex(), suffix))

            # 上传文件到七牛
            ret, info = put_up_datum(attachment.file_name, key_name, kind="stream")
            print(ret, info)
            if ret:
                attachment.after_upload_action(key_name, "sadgadsg")
                success_entities.append(attachment)

        # 更新上传成功的数据
        result = Attachment.batch_save(robot_session, success_entities)

        # 移走成功的文件.
        if result:
            file_name_list = [entity.file_name for entity in success_entities]
            fileFinished.batch_move(file_name_list)
    else:
        search_match_files(SEEK_DIRECTORY)


def main():
    """扫描文件入库——> 入库扫描上传 ——> 完毕之后再扫描.
    """

    init_redis_data()
    search_match_files(SEEK_DIRECTORY)

    # 纳入间隔时间后再次执行
    create_data = task.LoopingCall(upload_match_files, MATCH_FILES_LIMIT)
    create_data.start(MATCH_FILES_INTERVAL)
    reactor.run()


if __name__ == "__main__":
    """测试
    """

    main()
