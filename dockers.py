#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

import itertools
import os
import uuid

from twisted.internet import reactor, task

from common.warning import WarnMedia
from common.func import FileFinished, Utils, RedisService
from conf.data_config import robot_session, REDIS_CONFIG
from conf.logger_config import docker_data_log
from conf.regular_config import SEEK_DIRECTORY, DONE_DIRECTORY, \
    IGNORE_FILE_LIST, SKIP_README_FILE, ENABLE_FOLDER_RULE, MATCH_FILES_LIMIT, \
    MATCH_FILES_INTERVAL, USER_MAP_CONFIG, PLATE_MAP_CONFIG
from models.record import Attachment, Surplus
from upload import put_up_datum

fileFinished = FileFinished(SEEK_DIRECTORY, DONE_DIRECTORY)
redis_service = RedisService(db="files_md5sum", password=REDIS_CONFIG.get("password"))

media_path = os.path.dirname(os.path.abspath(__file__))
media_instance = WarnMedia(os.path.join(media_path, "media", "warn_pig.mp3"))


def init_redis_data():
    """初始化redis的数据.
    """

    attachment_entities = robot_session.query(Attachment, Attachment.id, Attachment.md5sum).all()
    for entity in attachment_entities:
        redis_service.set(entity.md5sum, entity.id)


def progress_handler(progress, total):
    """上传进度显示.
    """

    out_put = "%s%%" % str(int(float(progress) / float(total) * 100))
    docker_data_log.info(out_put)


def map_handler(_attachment):
    """使用map函数分发模式.

        :parameter _attachment 文件信息
    """

    _suffix = Utils.get_info_by_path(_attachment.file_name)[2]
    _key_name = ''.join((uuid.uuid4().get_hex(), _suffix))

    docker_data_log.info("=" * 80)
    docker_data_log.info("正在上传:%s" % _attachment.file_name)

    try:
        # 上传文件到七牛
        _ret, _info = put_up_datum(key=_key_name,
                                   kind="file",
                                   file_path=_attachment.file_name,
                                   progress_handler=progress_handler)
    except Exception, ex:
        docker_data_log.exception(ex)
    else:
        docker_data_log.info(_ret)
        docker_data_log.info(_info)
        if _ret and _ret["key"] == _key_name:
            try:
                attachment = _attachment.after_upload_action(_key_name, "")
                # 更新上传成功的数据
                robot_session.add(attachment)
                robot_session.commit()
            except Exception, ex:
                docker_data_log.exception(ex)
                robot_session.rollback()
            else:
                # 移走成功的文件.
                file_name_list = [attachment.file_name]
                try:
                    fileFinished.batch_move(file_name_list)
                except Exception, ex:
                    docker_data_log.exception(ex)


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
                author, plate = Utils.get_info_by_path(sub_path)[:2]
                plate = PLATE_MAP_CONFIG.get(plate)
            else:
                author, plate = '', 0

            # 如有重复记录到日志.
            md5sum = Utils.md5sum(sub_path)
            fid = redis_service.get(md5sum)
            if fid:
                Surplus(sub_path, plate=plate, author=author, md5sum=md5sum, fid=fid).save(robot_session)
                docker_data_log.info("skipping: %s ==> %s" % (author, sub_path))
                continue

            docker_data_log.info("indexing: %s ==> %s" % (author, sub_path))
            entity = Attachment(sub_path, plate=plate, author=author, md5sum=md5sum)
            robot_session.add(entity)
            robot_session.commit()
            redis_service.set(entity.md5sum, entity.id)


def upload_match_files(limit=5):
    """对结果入库的数据扫描, 并文件上传.

        :parameter limit: 检索数据数量
    """

    attachment_entities = robot_session.query(Attachment).filter(
        Attachment.status == 0).order_by(Attachment.id).limit(limit).all()

    if attachment_entities:
        # map(map_handler, attachment_entities)
        for attachment in attachment_entities:
            suffix = Utils.get_info_by_path(attachment.file_name)[2]
            key_name = ''.join((uuid.uuid4().get_hex(), suffix))

            errors = False
            docker_data_log.info("=" * 80)
            docker_data_log.info("正在上传:%s" % attachment.file_name)

            try:
                # 上传文件到七牛
                ret, info = put_up_datum(key=key_name,
                                         kind="file",
                                         file_path=attachment.file_name,
                                         progress_handler=progress_handler)
            except Exception, ex:
                errors = True
                docker_data_log.exception(ex)
            else:
                docker_data_log.info(ret)
                docker_data_log.info(info)
                if ret and ret["key"] == key_name:
                    try:
                        attachment = attachment.after_upload_action(key_name, "")
                        # 更新上传成功的数据
                        robot_session.add(attachment)
                        robot_session.commit()
                    except Exception, ex:
                        errors = True
                        docker_data_log.exception(ex)
                        robot_session.rollback()
                    else:
                        # 移走成功的文件.
                        file_name_list = [attachment.file_name]
                        try:
                            fileFinished.batch_move(file_name_list)
                        except Exception, ex:
                            errors = True
                            docker_data_log.exception(ex)

            # 如果异常, 报警并跳过
            if errors:
                media_instance.play()
                continue
    else:
        search_match_files(SEEK_DIRECTORY)


def main():
    """扫描文件入库——> 入库扫描上传 ——> 完毕之后再扫描.
    """

    # init_redis_data()
    # search_match_files(SEEK_DIRECTORY)

    # 纳入间隔时间后再次执行
    create_data = task.LoopingCall(upload_match_files, MATCH_FILES_LIMIT)
    create_data.start(MATCH_FILES_INTERVAL)
    reactor.run()


if __name__ == "__main__":
    """测试
    """

    main()
