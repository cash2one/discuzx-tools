#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

import itertools
import os
import time
import uuid

from twisted.internet import reactor, task

from common.func import FileFinished, Utils, RedisService
from common.warning import WarnMedia
from conf.data_config import robot_session, REDIS_CONFIG
from conf.logger_config import record_info, upload_info, upload_error
from conf.regular_config import SEEK_DIRECTORY, IGNORE_FILE_LIST, \
    SKIP_README_FILE, \
    ENABLE_FOLDER_RULE, MATCH_FILES_LIMIT, MATCH_FILES_INTERVAL, \
    USER_MAP_CONFIG, PLATE_MAP_CONFIG
from models.record import Attachment, Surplus
from upload import put_up_datum


def build_file_finished():
    if os.path.exists(SEEK_DIRECTORY):
        done_directory = os.path.join(os.path.dirname(SEEK_DIRECTORY), 'done')
        return FileFinished(SEEK_DIRECTORY, done_directory)


fileFinished = build_file_finished()
redis_md5sum = RedisService(db="files_md5sum",
                            password=REDIS_CONFIG.get("password"))
redis_unique = RedisService(db="files_unique",
                            password=REDIS_CONFIG.get("password"))

media_path = os.path.dirname(os.path.abspath(__file__))
media_instance = WarnMedia(os.path.join(media_path, "media", "warn_pig.mp3"))
upload_only_log = ("update bbs_attachment set status = 1, "
                   "upload_datetime = '%s' where id = %d;")


def init_redis_data(kind="md5sum"):
    """初始化redis的数据.

        :parameter kind: 操作类型
    """

    attachment_entities = robot_session.query(Attachment, Attachment.id,
                                              Attachment.md5sum,
                                              Attachment.key_name).all()

    # 清除既有数据.
    if kind.lower() == "md5sum":
        redis_md5sum.flush_db()
    elif kind.lower() == "unique":
        redis_unique.flush_db()

    for entity in attachment_entities:
        if kind.lower() == "md5sum" and entity.md5sum:
            redis_md5sum.set(entity.md5sum, entity.id)
        elif kind.lower() == "unique" and entity.key_name:
            redis_unique.set(entity.key_name, entity.id)


def progress_handler(progress, total):
    """上传进度显示.

        :parameter progress:
        :parameter total
    """

    out_put = "%s%%" % str(int(float(progress) / float(total) * 100))
    upload_info.info(out_put)


def map_handler(_attachment):
    """使用map函数分发模式.

        :parameter _attachment 文件信息
    """

    _suffix = Utils.get_info_by_path(_attachment.file_name)[2]
    _key_name = ''.join((uuid.uuid4().get_hex(), _suffix))

    upload_info.info("=" * 80)
    upload_info.info("正在上传:%s" % _attachment.file_name)

    try:
        # 上传文件到七牛
        _ret, _info = put_up_datum(key=_key_name,
                                   kind="file",
                                   file_path=_attachment.file_name,
                                   progress_handler=progress_handler)
    except Exception, ex:
        upload_info.exception(ex)
    else:
        upload_info.info(_ret)
        upload_info.info(_info)
        if _ret and _ret["key"] == _key_name:
            try:
                attachment = _attachment.after_upload_action("")
                # 更新上传成功的数据
                robot_session.add(attachment)
                robot_session.commit()
            except Exception, ex:
                robot_session.rollback()
                upload_info.exception(ex)
                upload_error.info(upload_only_log % (
                    _attachment.upload_datetime, _attachment.id))
            else:
                # 移走成功的文件.
                file_name_list = [attachment.file_name]
                try:
                    fileFinished.batch_move(file_name_list)
                except Exception, ex:
                    upload_info.exception(ex)
            finally:
                robot_session.close()


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
                if base_name not in itertools.chain(
                        PLATE_MAP_CONFIG.keys(),
                        USER_MAP_CONFIG.keys()):
                    continue

            search_match_files(sub_path)
        else:

            # 跳过计划的文件列表.
            if SKIP_README_FILE:
                ignore_file_list = map(lambda x: x.lower(), IGNORE_FILE_LIST)
                if ignore_file_list and os.path.basename(
                        sub_path).lower() in ignore_file_list:
                    continue

            # 版块与作者(plate=0, author='')的对应.
            if ENABLE_FOLDER_RULE:
                author, plate = Utils.get_info_by_path(sub_path)[:2]
                plate = PLATE_MAP_CONFIG.get(plate)
            else:
                author, plate = '', 0

            # 如有重复记录到日志.
            md5sum = Utils.md5sum(sub_path)
            fid = redis_md5sum.get(md5sum)
            if fid:
                Surplus(sub_path, plate=plate, author=author, md5sum=md5sum,
                        fid=fid).__save(robot_session)
                record_info.info("skipping: %s ==> %s" % (author, sub_path))
                continue

            record_info.info("indexing: %s ==> %s" % (author, sub_path))

            suffix = Utils.get_info_by_path(sub_path)[2]
            key_name = ''.join((uuid.uuid4().get_hex(), suffix))
            entity = Attachment(
                sub_path, key_name, plate=plate, author=author, md5sum=md5sum)
            robot_session.add(entity)
            robot_session.commit()
            redis_md5sum.set(entity.md5sum, entity.id)


def upload_match_files(limit=5, loops=True):
    """对结果入库的数据扫描, 并文件上传.

        :parameter limit: 检索数据数量
        :parameter loops: 是否执行完数据再扫描
    """

    attachment_entities = robot_session.query(Attachment).filter(
        Attachment.status == 0).order_by(Attachment.id).limit(limit).all()

    if attachment_entities:
        # map(map_handler, attachment_entities)
        for attachment in attachment_entities:
            errors = False
            upload_info.info("=" * 80)
            upload_info.info("正在上传:%s" % attachment.file_name)

            try:
                # 上传文件到七牛
                ret, info = put_up_datum(
                    key=attachment.key_name,
                    kind="file",
                    file_path=attachment.file_name,
                    progress_handler=progress_handler)
            except Exception, ex:
                errors = True
                upload_info.exception(ex)
            else:
                upload_info.info(ret)
                upload_info.info(info)
                if ret and ret["key"] == attachment.key_name:
                    try:
                        attachment = attachment.after_upload_action("")
                        # 更新上传成功的数据
                        robot_session.add(attachment)
                        robot_session.commit()
                    except Exception, ex:
                        errors = True
                        robot_session.rollback()
                        upload_info.exception(ex)
                        upload_error.log(upload_only_log % (
                            attachment.upload_datetime, attachment.id))
                    else:
                        # 移走成功的文件.
                        file_name_list = [attachment.file_name]
                        try:
                            fileFinished.batch_move(file_name_list)
                        except Exception, ex:
                            errors = True
                            upload_info.exception(ex)
                    finally:
                        robot_session.close()

            # 如果异常, 报警并跳过
            if errors:
                media_instance.play()
                continue
    else:
        # 如果无数据静默五分钟
        time.sleep(5 * 60)
        if loops:
            search_match_files(SEEK_DIRECTORY)


def update_name_files(limit=20):
    """更新导入库的索引文件.

        :parameter limit: 每次限制数
    """

    attachment_entities = robot_session.query(Attachment).filter(
        Attachment.key_name == "", Attachment.status == 0).order_by(
        Attachment.id).limit(limit).all()

    result = False
    if attachment_entities:
        for attachment in attachment_entities:
            suffix = Utils.get_info_by_path(attachment.file_name)[2]

            # 生成唯一标识, 防冲突可能从cache比对已有值.
            key_name = ""
            while True:
                key_name = ''.join((uuid.uuid4().get_hex(), suffix))
                fid = redis_md5sum.get(key_name)
                if not fid:
                    break
            attachment.key_name = key_name

            # 放入cache供后续比对.
            redis_md5sum.set(key_name, 1)

        try:
            robot_session.add_all(attachment_entities)
            robot_session.commit()
        except Exception, ex:
            print(ex)
            robot_session.rollback()
        else:
            print("OK")
        finally:
            robot_session.close()
    else:
        result = True

    return result


def main():
    """扫描文件入库——> 入库扫描上传 ——> 完毕之后再扫描.
    """

    init_redis_data()
    search_match_files(SEEK_DIRECTORY)

    # 纳入间隔时间后再次执行
    create_data = task.LoopingCall(upload_match_files, MATCH_FILES_LIMIT, True)
    create_data.start(MATCH_FILES_INTERVAL)
    reactor.run()


def minor():
    """仅对已扫描的数据数据执行上传操作.
    """

    while True:
        upload_match_files(MATCH_FILES_LIMIT, False)


def repair():
    """循环修复, 直至无修复数据退出.
    """

    init_redis_data(kind="unique")

    while True:
        result = update_name_files(200)
        if result:
            print("OK, 修复完成.")
            break


if __name__ == "__main__":
    """测试并跑任务, 注意以下三者的区别.
    """

    # main()
    minor()
    # repair()
