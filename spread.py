#!usr/bin/env python
# coding: utf-8

"""任务执行的入口.
"""

from __future__ import unicode_literals, print_function

import os
import random

from twisted.internet import task
from twisted.internet import reactor

from conf.data_config import robot_session
from conf.logger_config import posting_data_log
from conf.regular_config import USER_MAP_CONFIG
from models.record import Attachment, Thread
from posting.manager import spread_info


def spread_match_files(limit=5):
    """对结果入库的数据扫描, 并文件上传.

        :parameter limit: 扫描数据数量
    """

    attachment_entities = robot_session.query(Attachment).filter(
        Attachment.status == 1).order_by(Attachment.id).limit(limit).all()

    def author_uid_and_name(real_name):
        """由真实姓名拼音获取论坛账户(账户Id,账户名称)
        """

        authors = USER_MAP_CONFIG.get(real_name).split("|")
        return int(authors[0]), authors[2]

    if attachment_entities:
        for attachment in attachment_entities:
            # 构建主题, 帖子, 附件
            file_base_name = os.path.basename(attachment.file_name)
            subject = message = os.path.splitext(file_base_name)[0]
            author = author_uid_and_name(attachment.author)
            fid = attachment.plate

            posting_data_log.info("=" * 80)
            posting_data_log.info("正在发帖:%s" % file_base_name)

            tid, pid, aid = spread_info(subject, message, author, fid,
                                        file_name=file_base_name,
                                        attachment=attachment.key_name)

            # 更新发帖成功的数据状态, 保存记录
            attachment.status = 2
            robot_record = Thread(tid, pid, aid, attachment.id)

            robot_session.add(attachment)
            robot_session.add(robot_record)
            robot_session.commit()


action_data_config = (
    # 任务, 数据量, 时间间隔
    (spread_match_files, 2, 5.0),
    # (None, 1, 5.0),
)


def main():
    """事件模拟任务调度.
    """

    for data_item in action_data_config:
        if type(data_item[0]) == 'function':
            create_data = task.LoopingCall(data_item[0], data_item[1])
            create_data.start(data_item[2])

    reactor.run()


def minor():
    """仅对已扫描的数据数据执行上传操作.
    """

    while True:
        spread_match_files(1)


def spread_only():
    """仅仅发帖部分.
    """

    interval = (20, 30, 50, 70, 100)
    limit = (2, 3, 5, 7)

    # 纳入间隔时间后再次执行
    create_data = task.LoopingCall(spread_match_files, random.choice(limit))
    create_data.start(random.choice(interval))
    reactor.run()


if __name__ == '__main__':
    """测试并跑任务, 注意以下三者的区别.
    """

    # main()
    # minor()
    spread_only()
