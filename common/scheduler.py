#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals, print_function

import time
import random
import datetime
from functools import wraps, partial

from twisted.internet import reactor

hours = [23, 0, 1, 2, 3, 4, 5, 6, 7]


def skip_hours(func):
    @wraps(func)
    def returned_wrapper(*args, **kwargs):
        now = datetime.datetime.now().time()
        if now.hour in hours:
            time.sleep(60 * 60)
        else:
            if args and not kwargs:
                func(*args)
            elif args and kwargs:
                func(*args, **kwargs)
            else:
                func()

    return returned_wrapper


class NoInterval(object):
    """没固定间隔的间隔执行.
    """

    def __init__(self, intervals):
        self.intervals = intervals

    def echo(self, timeout):
        self.work()
        cb = partial(self.echo, timeout=random.choice(self.intervals))
        reactor.callLater(timeout, cb)

    def run(self):
        self.echo(timeout=random.choice(self.intervals))
        reactor.run()

    def work(self):
        """子类实现.
        """
        pass

    @staticmethod
    def demo(func, intervals):
        """仅实际操作.
        """

        class _Demo(NoInterval):
            def work(self):
                func()

        _demo = _Demo(intervals)
        _demo.run()


class Scheduler(object):
    """任务计划.
    """

    def __init__(self, time_list):
        """
            :parameter time_list: 形式如:[(18, 30, 00), (19, 00, 00)]
        """

        if isinstance(time_list, list):
            time_list.sort()
            self.time_list = time_list
        else:
            raise TypeError("传入参数类型错误,形式要求为:[(<时>,<分>,<秒>),]")

    def _time_origin(self):
        """用于从时间列表中选当前时间的下个时间执行点.
        """

        index = 0
        time_origin = time.localtime()
        ss = (time_origin.tm_hour, time_origin.tm_min, time_origin.tm_sec)
        while True:
            if self.time_list[index] < ss:
                index += 1
            else:
                yield index, self.time_list[index]

    def _generate_time_point(self, index=0, break_loop=False):
        """轮询到每个时间点.

            :parameter index            时间列表起始执行点.
            :parameter break_loop       用于time_list时间点执行完毕是否退出, 默认False不退出, 循环每一天.
        """

        count = len(self.time_list)
        while True:
            yield self.time_list[index]
            index += 1

            if index == count:
                if break_loop:
                    break
                else:
                    index = 0

    @staticmethod
    def make_timestamp(hour, minute, second=0):
        """转换传入time_list参数值.

            :parameter hour
            :parameter minute
            :parameter second
        """
        now_time = time.localtime()
        _time = time.mktime(time.strptime(
            "%s-%s-%s %s:%s:%s" % (now_time.tm_year, now_time.tm_mon, now_time.tm_mday, hour, minute, second),
            "%Y-%m-%d %H:%M:%S"))

        return int(_time)

    @classmethod
    def work(cls):
        return NotImplemented

    def start(self):
        """子类启动入口.
        """

        time_index = self._time_origin().next()[0]

        while True:
            now_time = time.localtime()
            time_next = self._generate_time_point(index=time_index).next()  # 不传入break_loop的参数.
            unix_time = int(time.mktime(now_time))
            unix_next = self.make_timestamp(time_next[0], time_next[1], time_next[2])

            interval = unix_next - unix_time
            if interval < 0:
                interval += 86400

            time.sleep(interval)
            self.work()

    def test(self):
        """测试.
        """

        now_time = time.localtime()
        time_index = self._time_origin().next()[0]

        for time_next in self._generate_time_point(index=time_index, break_loop=True):  # 传入break_loop = True的参数.
            unix_time = int(time.mktime(now_time))
            unix_next = self.make_timestamp(time_next[0], time_next[1], time_next[2])

            interval = unix_next - unix_time
            if interval < 0:
                interval += 86400

            print(unix_next - unix_time)
            self.work()

    def origin(self):
        """测试, 仅为测试时间执行计划列表中的起点时间而用.
        """

        print(self.time_list)
        time_index = self._time_origin().next()[0]
        # for x in self._generate_time_point(index=time_index, break_loop=True):  # 传入break_loop = True的参数.

        counter = 0
        for x in self._generate_time_point(index=time_index):
            if counter == 20:
                break

            print("%s:%s:%s" % x)
            self.work()
            counter += 1


class Demo(Scheduler):
    def work(self):
        print("I'am Working...\n")


if __name__ == "__main__":
    """测试.
    """

    lst = [(8, 30, 00), (18, 30, 00), (16, 30, 00), (19, 00, 00), (13, 00, 00)]
    demo = Demo(time_list=lst)
    # demo.test()
    demo.origin()
