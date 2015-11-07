#!usr/bin/env python
# coding: utf-8

"""任务执行的入口.
"""

from __future__ import unicode_literals, print_function

import os

from twisted.internet import task
from twisted.internet import reactor

from conf.data_config import robot_session
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

            tid, pid, aid = spread_info(subject, message, author, fid,
                                        file_name=file_base_name,
                                        attachment=attachment.key_name)

            # 保存记录
            robot_record = Thread(tid, pid, aid, attachment.__id)
            Thread.save(robot_session, robot_record)


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


if __name__ == '__main__':
    """测试
    """

    main()
