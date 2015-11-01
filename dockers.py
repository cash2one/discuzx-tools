#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

import os
import uuid
import itertools

from twisted.internet import task
from twisted.internet import reactor

from conf.data_config import robot_session
from conf.regular_config import SEEK_DIRECTORY, DONE_DIRECTORY, \
    MATCH_FILES_LIMIT, MATCH_FILES_INTERVAL, USER_MAP_CONFIG, PLATE_MAP_CONFIG

from common.func import FileFinished, Utils
from models.record import Attachment, Surplus
from upload.common import put_up_datum

fileFinished = FileFinished(SEEK_DIRECTORY, DONE_DIRECTORY)


def search_match_files(directory):
    """对指定的目录文件扫描, 并结果入库.
    """

    files_entities = []
    files_md5sum_dict = {}  # key为md5sum, value为fid

    # 扫描文件
    for i in os.listdir(directory):
        sub_path = os.path.join(directory, i)
        if os.path.isdir(sub_path):
            base_name = os.path.basename(sub_path).lower()

            # 跳过未适配的版块和作者.
            if base_name not in itertools.chain(PLATE_MAP_CONFIG.keys(), USER_MAP_CONFIG.keys()):
                continue

            search_match_files(sub_path)
        else:
            # 跳过注释的readme.txt文件.
            if os.path.basename(sub_path).lower() == "readme.txt":
                continue

            # 版块与作者(plate=0, author='')的对应.
            plate, author = Utils.get_info_by_path(sub_path)[:2]
            plate = PLATE_MAP_CONFIG.get(plate)
            md5sum = Utils.md5sum(sub_path)

            # 如有重复记录到日志.
            if md5sum in files_md5sum_dict.keys():
                fid = files_md5sum_dict.get(md5sum, 0)
                Surplus(sub_path, plate=plate, author=author, md5sum=md5sum, fid=fid).save(robot_session)
                continue

            entity = Attachment(sub_path, plate=plate, author=author, md5sum=md5sum)
            files_entities.append(entity)

    Attachment.batch_save(robot_session, files_entities)


def update_match_files(limit=5):
    """对结果入库的数据扫描, 并文件上传.
    """

    success_entities = []
    attachment_entities = robot_session.query(Attachment).filter(
        Attachment.status == 0).order_by(Attachment.id).limit(limit).all()

    if attachment_entities:
        for attachment in attachment_entities:
            suffix = Utils.get_info_by_path(attachment.file_name)[2]
            key_name = ''.join((uuid.uuid4().get_hex(), suffix))
            # TODO: 报错异常.
            ret, info = put_up_datum(attachment.file_name, key_name)
            print(ret, info)

            ret = True
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

    search_match_files(SEEK_DIRECTORY)

    # 纳入间隔时间后再次执行
    create_data = task.LoopingCall(update_match_files, MATCH_FILES_LIMIT)
    create_data.start(MATCH_FILES_INTERVAL)
    reactor.run()


if __name__ == "__main__":
    """测试
    """

    main()
