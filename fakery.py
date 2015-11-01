#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""以服务的形式运行模拟用户操作.
"""

from __future__ import unicode_literals, print_function

import time
import random
import string

from twisted.internet import task
from twisted.internet import reactor
from conf.data_config import robot_session
from conf.logger_config import faker_data_log
from common.func import Utils
from register.factory import FakeMember, FakePost
from models.record import Member
from models.remote import CommonMember, CenterMember


def fake_member(gen_data_count=1):
    """创建虚拟账户.

        gen_data_count的取值建议不要大, 因为不希望在时间点上跳跃性增长.
    """

    common_member_entities_list = []
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

        try:
            common_member = CommonMember(__groupid=10,
                                         __username=username,
                                         __password=fake_password,
                                         __email=entity["email"],
                                         __regdate=int(time.time()))
            CommonMember.add(common_member)

            center_member = CenterMember(__salt=salt,
                                         __username=username,
                                         __password=hash_password,
                                         __email=entity["email"],
                                         __regdate=int(time.time()),
                                         __uid=common_member.__uid)
            CenterMember.add(center_member)
        except Exception, ex:
            faker_data_log.exception(ex)
        else:
            member = Member(username, password, entity["email"], common_member.__uid)
            common_member_entities_list.append(member)

        Member.batch_save(robot_session, common_member_entities_list)


def fake_post(gen_data_count=1):
    """虚拟对主题回帖.
    """

    for post in FakePost().generate(gen_data_count):
        print(post)


action_data_config = (
    # 任务, 数据量, 时间间隔
    (fake_member, 1, 5.0),
    (None, None, 5.0),
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
    # main()
    fake_member()
