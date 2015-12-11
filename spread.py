#!usr/bin/env python
# coding: utf-8

"""任务执行的入口.
"""

from __future__ import unicode_literals, print_function

import os
import time
import random

from twisted.internet import task, reactor

from conf.data_config import robot_session
from conf.logger_config import post_info
from conf.regular_config import USER_MAP_CONFIG
from common.scheduler import partial, skip_hours, NoInterval
from models.record import Attachment, Thread
from posting.manager import spread_info

limits = (2, 3, 5, 7)
intervals = (20, 30, 50, 70, 100)


@skip_hours
def spread_match_files(limit=5):
    """对结果入库的数据扫描, 并文件上传.

        :parameter limit: 扫描数据数量
    """

    attachment_entities = robot_session.query(Attachment).filter(
        Attachment.status == 1).order_by(Attachment.id).limit(limit).all()

    def author_uid_and_name(real_name):
        """由真实姓名拼音获取论坛账户(账户Id,账户名称)

            :parameter real_name: 账户名称
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

            post_info.info("=" * 80)
            post_info.info("正在发帖:%s" % file_base_name)

            tid, pid, aid = spread_info(subject, message, author, fid,
                                        file_name=file_base_name,
                                        attachment=attachment.key_name)

            if tid and pid:
                try:
                    # 更新发帖成功的数据状态, 保存记录
                    attachment.status = 2
                    robot_record = Thread(tid, pid, fid, aid, attachment.id)

                    robot_session.add(attachment)
                    robot_session.add(robot_record)
                    robot_session.commit()
                    post_info.info("发帖成功: OK.")
                except Exception, ex:
                    robot_session.rollback()
                    post_info.exception(ex)
                finally:
                    robot_session.close()
            else:
                post_info.info("发帖失败: Error.")
    else:
        # 如果无数据静默五分钟
        time.sleep(5 * 60)


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
    """仅对已扫描的数据数据执行发帖操作.
    """

    while True:
        spread_match_files(1)


def spread_only():
    """仅仅发帖部分.
    """

    # 纳入间隔时间后再次执行
    create_data = task.LoopingCall(spread_match_files, limits[0])
    create_data.start(intervals[0])
    reactor.run()


if __name__ == '__main__':
    """测试并跑任务, 注意以下三者的区别.
    """

    # main()
    # minor()
    # spread_only()
    cb = partial(spread_match_files, gen_data_count=random.choice(limits))
    NoInterval.demo(cb, intervals=random.choice(intervals))
