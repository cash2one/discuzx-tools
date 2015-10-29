#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

import os
import uuid
from conf.data_config import robot_session
from conf.regular_config import SEEK_DIRECTORY, DONE_DIRECTORY, LIMIT_MATCH_FILES
from common.func import FileFinished
from models.record import Attachment
from upload.common import put_up_datum

fileFinished = FileFinished(SEEK_DIRECTORY, DONE_DIRECTORY)


def search_match_files(directory):
    """对指定的目录文件扫描, 并结果入库.
    """

    files_entities = []

    # 扫描文件
    for i in os.listdir(directory):
        sub_path = os.path.join(directory, i)
        if os.path.isdir(sub_path):
            search_match_files(sub_path)
        else:
            # TODO:版块与作者(plate=0, author='')的对应.
            entity = Attachment(sub_path, plate=0, author='')
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
            key_name = uuid.uuid4().get_hex()
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


if __name__ == "__main__":
    """测试
    """

    update_match_files(LIMIT_MATCH_FILES)
