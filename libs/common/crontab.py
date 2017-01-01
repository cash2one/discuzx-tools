#!usr/bin/env python
# coding:utf-8

from __future__ import print_function

import datetime

from twisted.internet import task, reactor

from scheduler import skip_hours, NoInterval


@skip_hours
def echo():
    now = datetime.datetime.now().time()
    print(now)


def only():
    create_data = task.LoopingCall(echo)
    create_data.start(60)
    reactor.run()


if __name__ == "__main__":
    try:
        # only()
        NoInterval.demo(lambda: print(datetime.datetime.now()), (1, 2, 3))
    except KeyboardInterrupt:
        exit()
