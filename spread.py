#!usr/bin/env python
# coding: utf-8

"""任务执行的入口.
"""

from __future__ import unicode_literals, print_function

import time
import random
import string

from twisted.internet import task
from twisted.internet import reactor
from common.func import FileProcess
from conf.data_config import robot_session
from models.record import Attachment, Thread
from models.remote import ForumPost, ForumThread, ForumAttachment


def post_thread():
    """发主题表操作.
    """

    try:
        forum_attachment = ForumAttachment()
        ForumAttachment.add(forum_attachment)

        forum_thread = ForumThread()
        forum_post = ForumPost(forum_thread)
        ForumThread.add(forum_thread)
        ForumPost.add(forum_post)
    except Exception, ex:
        print(ex)
    else:
        print("OK")


def post_content(tid):
    """发帖子操作帖子表.

        tid: 帖子ID
    """

    try:
        forum_post = ForumPost(tid=tid)
        ForumPost.add(forum_post)
    except Exception, ex:
        print(ex)
    else:
        print("OK")


def spread_match_files(limit=5):
    """对结果入库的数据扫描, 并文件上传.
    """

    attachment_entities = robot_session.query(Attachment).filter(
        Attachment.status == 1).order_by(Attachment.id).limit(limit).all()

    if attachment_entities:
        for attachment in attachment_entities:
            # 构建附件
            # 构建主题
            forum_thread = None
            # 构建帖子
            # 保存记录
            Thread(thread_id=forum_thread.__id, attachment_id=attachment.id)


action_data_config = (
    # 任务, 数据量, 时间间隔
    (post_thread, 1, 5.0),
    (post_content, 1, 5.0),
)


def main():
    """事件模拟任务调度.
    """

    for data_item in action_data_config:
        if type(data_item[0]) == 'function':
            create_data = task.LoopingCall(data_item[0], data_item[1])
            create_data.start(data_item[2])

    reactor.run()


if __name__ == '__main__':
    """测试
    """

    main()
