#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""以服务的形式运行模拟用户操作.
"""

from __future__ import unicode_literals, print_function

import time
import datetime
import random
import string

from twisted.internet import task

from twisted.internet import reactor

from conf.data_config import robot_session, forum_session
from conf.logger_config import user_info, recommend_info
from common.func import Utils, CacheService
from register.factory import FakeMember, FakeRecommend, FakePost
from models.record import Member, Thread
from models.remote import CommonMember, CenterMember, ForumThread, ForumMemberRecommend


def cache_thread_member():
    """从数据库载入数据(thread,member).
    """

    CacheService.cache_data_delete_model("forum_thread")
    CacheService.cache_data_delete_model("common_member")

    forum_thread_entities = robot_session.query(Thread).all()
    common_member_entities = robot_session.query(Member).all()

    CacheService.cache_data_import_model(forum_thread_entities, "forum_thread")
    CacheService.cache_data_import_model(common_member_entities, "common_member")


def fake_member(gen_data_count=1):
    """创建虚拟账户.

        gen_data_count的取值建议不要大, 因为不希望在时间点上跳跃性增长.
        :parameter gen_data_count: 生成数据数量
    """

    for entity in FakeMember().generate(gen_data_count):
        username = entity["username"].lower()

        length = random.randint(6, 20)
        random_string = ''.join((entity["password"], str(entity["assist_number"])))
        random_string = [random.choice(random_string) for _ in range(length)]
        password = ''.join(random_string)

        # 用户中心md5后的实际密码.
        salt = "".join([random.choice(string.ascii_lowercase + string.digits) for _ in range(6)])
        hash_password = Utils.dz_uc_md5(password, salt)

        # 会员表md5后的伪密码.
        fake_password = Utils.md5(str(random.randint(10 * 9, 10 ** 10 - 1)))

        user_info.info("=" * 80)
        user_info.info("正在注册账户:%s" % username)

        try:
            common_member = CommonMember(__groupid=10,
                                         __username=username,
                                         __password=fake_password,
                                         __email=entity["email"],
                                         __regdate=int(time.time()))
            forum_session.add(common_member)
            forum_session.flush()
            uid = common_member.__uid

            center_member = CenterMember(__salt=salt,
                                         __username=username,
                                         __password=hash_password,
                                         __email=entity["email"],
                                         __regdate=int(time.time()),
                                         __uid=uid)

            forum_session.add(center_member)
            forum_session.commit()

            member = Member(username, password, entity["email"], uid)
            robot_session.add(member)
            robot_session.commit()
        except Exception, ex:
            user_info.exception(ex)
            user_info.info("注册账户失败: Error.")
            forum_session.rollback()
            robot_session.rollback()
        else:
            user_info.info("注册账户成功: OK.")
        finally:
            forum_session.close()
            robot_session.close()


def fake_recommend(gen_data_count=1):
    """虚拟对主题回帖.

        :parameter gen_data_count: 生成数据数量
    """

    for entity in FakeRecommend().generate(gen_data_count):
        print(entity)
        tid = entity["tid"]
        uid = entity["uid"]
        opinion = entity["opinion"]

        print(tid,uid,opinion)

        recommend_info.info("=" * 80)
        recommend_info.info("(%s)正在评帖(%s)" % (uid, tid))

        # 查询是否顶过帖
        recommend_entities = forum_session.query(ForumMemberRecommend).filter(
            ForumMemberRecommend.__tid == tid,
            ForumMemberRecommend.__recommenduid == uid).all()

        if recommend_entities:
            recommend_info.info("返回:之前已评过该帖！")
            continue

        try:
            forum_member_recommend = ForumMemberRecommend(__tid=tid, __recommenduid=uid, __dateline=int(time.time()))
            forum_thread = forum_session.query(ForumThread).filter(ForumThread.__tid == tid).first()
            forum_thread.__views += 1  # 查看次数
            forum_thread.__recommends += 1  # 推荐指数
            if opinion < 85:
                forum_thread.__recommend_add += 1  # 支持人数
            else:
                forum_thread.__recommend_sub += 1  # 反对人数

            forum_session.add(forum_member_recommend)
            forum_session.add(forum_thread)
            forum_session.commit()
        except Exception, ex:
            recommend_info.exception(ex)
            recommend_info.info("评帖失败: Error.")
            forum_session.rollback()
        else:
            recommend_info.info("评帖成功: OK.")
        finally:
            forum_session.close()


def fake_post(gen_data_count=1):
    """虚拟对主题回帖.

        :parameter gen_data_count: 生成数据数量
    """

    for post in FakePost().generate(gen_data_count):
        print(post)


action_data_config = (
    # 任务, 数据量, 时间间隔
    (fake_member, 1, 5.0),
    (fake_recommend, 1, 5.0),
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
    """仅对已扫描的数据数据执行上传操作.
    """

    cache_thread_member()

    while True:
        print(datetime.datetime.now())
        fake_member(1)
        # fake_recommend(1)
        # time.sleep(60)


def fake_member_only():
    """仅仅注册部分.
    """

    interval = (30, 50, 70, 100, 150)
    limit = (1, 2, 3, 4)

    # 纳入间隔时间后再次执行
    create_data = task.LoopingCall(fake_member, random.choice(limit))
    create_data.start(random.choice(interval))
    reactor.run()


def fake_recommend_only():
    """仅仅顶贴部分.
    """

    cache_thread_member()

    interval = (30, 50, 70, 80, 110)
    limit = (2, 3, 4, 5)

    # 纳入间隔时间后再次执行
    create_data = task.LoopingCall(fake_recommend, random.choice(limit))
    create_data.start(random.choice(interval))
    reactor.run()


if __name__ == '__main__':
    # main()
    # minor()
    fake_member_only()
    fake_recommend_only()
