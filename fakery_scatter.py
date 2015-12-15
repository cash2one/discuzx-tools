#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""修正数据库数据.
"""

from __future__ import unicode_literals, print_function

import time
import random
import traceback
from conf.data_config import robot_session, forum_session
from models.record import Thread, Member
from register.factory import FakeMemberStatus
from models.remote import ForumThread, ForumPost, CommonMemberStatus


def scat_content_to_user():
    """分发自动发帖数据到部分用户.
    """

    print("=" * 80)
    print("Info: Work is now being prepared.")

    split_groups = 5
    username = 'rongtang'

    # uid在[56,200]之间.
    thread_range = (56, 200)

    # create_datetime在["2015-11-20 00:00:00","2015-11-21 23:00:00"]之间.
    datetime_range = ('2015-11-20 00:00:00', '2015-11-21 23:00:00')

    try:
        # 查询出分发用户数据.
        author_entities = robot_session.query(Member).filter(
                Member.dz_uid.between(thread_range[0], thread_range[1])).all()
        author_list = [(author.dz_uid, author.username) for author in author_entities]

        # 查询出自动发帖数据.
        thread_logs = robot_session.query(Thread.thread_id, Thread.post_id).filter(
                Thread.create_datetime.between(datetime_range[0], datetime_range[1])).all()

        post_ids = [thread_entity.post_id for thread_entity in thread_logs]
        thread_ids = [thread_entity.thread_id for thread_entity in thread_logs]

        unit_entities = []

        # 分发用户(荣堂)数据.
        thread_entities = forum_session.query(ForumThread).filter(ForumThread.__author == username).all()
        threads_total = len(thread_entities)

        thread_normal, thread_moved, thread_retain = 0, 0, 0
        print("Info: threads_total = %s." % threads_total)
        print("=" * 80)

        for index, thread_entity in enumerate(thread_entities):
            print("Info: %s %s%%." % (index, str(int(float(index) / float(threads_total) * 100))))

            # 只分发自动发帖数据, 跳过正常从网站发出数据.
            if thread_entity.__tid not in thread_ids:
                thread_normal += 1
                continue

            # 将用户(荣堂)数据分五份(保留一份给本人,四份分发).
            if index % split_groups == 0:
                thread_retain += 1
                continue

            # 更新主题用户信息
            author = random.choice(author_list)
            thread_entity.__author = author[1],
            thread_entity.__authorid = author[0],

            # 更新帖子用户信息
            post_entity = forum_session.query(ForumPost).filter(
                    ForumPost.__tid == thread_entity.__tid).first()

            if not post_entity or post_entity.__pid not in post_ids:
                continue

            post_entity.__author = author[1],
            post_entity.__authorid = author[0],

            unit_entities.append(thread_entity)
            unit_entities.append(post_entity)

        thread_moved = len(unit_entities) / 2
        forum_session.add_all(unit_entities)
        forum_session.commit()
    except Exception, ex:
        print(ex)
        traceback.print_exc()
        forum_session.rollback()
    else:
        print("=" * 80)
        print("Info: About User(%s) In %s Info:" % (username, datetime_range))
        print("Info: 论坛正常帖数 %(d)s 分发出贴数 %(d)s 保留的帖数" % {"d": " " * 20})
        print("Info: thread_normal = %d thread_moved = %d thread_retain = %d."
              % (thread_normal, thread_moved, thread_retain))
        print("Info: Well Done.")
    finally:
        forum_session.close()
        print("All Work Have Finished.")
        print("=" * 80)


def fix_member_miss_status():
    """修复自动注册的用户缺失状态数据.
    """

    print("=" * 80)
    try:
        print("Info: Work is now being prepared.")

        # 自动注册用户.
        robot_member_entities = robot_session.query(Member).all()
        gen_data_count = len(robot_member_entities)

        # 补充自注册数据.
        member_status_data = FakeMemberStatus().generate(gen_data_count)
        member_status_list = [entity for entity in member_status_data]

        print("Info: member_entities_total = %s." % gen_data_count)

        member_status_entities = []
        for index, member_entity in enumerate(robot_member_entities):
            print("Info: %s %s%%." % (index, str(int(float(index) / float(gen_data_count) * 100))))

            status_data = member_status_list[index]
            member_status = CommonMemberStatus(__uid=member_entity.dz_uid,
                                               __regip=status_data['reg_ip'],
                                               __lastip=status_data['last_ip'],
                                               __lastvisit=int(time.time()),
                                               __lastactivity=int(time.time()))
            member_status_entities.append(member_status)

        forum_session.add_all(member_status_entities)
        forum_session.commit()
    except Exception, ex:
        print(ex)
        traceback.print_exc()
        forum_session.rollback()
    else:
        print("Info: Well Done.")
    finally:
        forum_session.close()
        print("All Work Have Finished.")
        print("=" * 80)


if __name__ == '__main__':
    """执行模块任务.
    """

    # scat_content_to_user()
    fix_member_miss_status()
