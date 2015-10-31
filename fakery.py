#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""以服务的形式运行模拟用户操作.
"""

from __future__ import unicode_literals, print_function

from twisted.internet import task
from twisted.internet import reactor


action_data_config = (
    # 任务, 数据量, 时间间隔
    (None, None, 5.0),
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
    main()
