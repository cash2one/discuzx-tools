#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""以服务的形式运行模拟用户操作.
"""

from __future__ import unicode_literals, print_function

import datetime
import random

from twisted.internet import task, reactor

from conf.data_config import robot_session
from conf.logger_config import faker_post_info, faker_post_error
from register.factory import FakePost
from models.record import Post
from models.submeter import cache_thread_member
from posting.manager import spread_post

faker_post_only = "INSERT INTO bbs_post(uid,tid,pid,create_datetime) VALUES(%s,%s,%s,'%s');"


def fake_post(gen_data_count=1):
    """虚拟对主题回帖.

        :parameter gen_data_count: 生成数据数量
    """

    for entity in FakePost().generate(gen_data_count):
        print(entity)

        uid = entity["uid"]
        tid = entity["tid"]
        fid = entity["fid"]
        username = entity["username"]
        message = entity["message"]

        print(uid, tid, fid, username, message)

        faker_post_info.info("=" * 80)
        faker_post_info.info("(%s)正在回帖(%s)" % (username, tid))

        pid = spread_post(uid, tid, fid, username, message)

        if pid:
            try:
                post = Post(uid, tid, pid, fid)
                robot_session.add(post)
                robot_session.commit()
            except Exception, ex:
                robot_session.rollback()
                faker_post_info.exception(ex)
                faker_post_info.info("回帖成功但记录失败: OK.")
                time_now = datetime.datetime.now().strftime("%Y-%m-%d %X")
                faker_post_error.info(faker_post_only % (uid, tid, pid, time_now))
            else:
                faker_post_info.info("回帖成功: OK.")
            finally:
                robot_session.close()
        else:
            faker_post_info.info("回帖失败: Error.")


action_data_config = (
    # 任务, 数据量, 时间间隔
    (fake_post, 1, 5.0),
)


def main():
    """事件模拟任务调度.
    """

    cache_thread_member()

    for data_item in action_data_config:
        if type(data_item[0]) == 'function':
            create_data = task.LoopingCall(data_item[0], data_item[1])
            create_data.start(data_item[2])

    reactor.run()


def minor():
    """仅回贴部分.
    """

    cache_thread_member()

    while True:
        print(datetime.datetime.now())
        fake_post(1)
        # time.sleep(60)


def fake_post_only():
    """仅仅回贴部分.
    """

    cache_thread_member()

    interval = (30, 50, 70, 80)
    limit = (1, 2, 3)

    # 纳入间隔时间后再次执行
    create_data = task.LoopingCall(fake_post, random.choice(limit))
    create_data.start(random.choice(interval))
    reactor.run()


if __name__ == '__main__':
    # main()
    # minor()
    fake_post_only()
