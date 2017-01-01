#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals, print_function


class TimeMeasure(object):
    __abstract__ = True

    def __init__(self, minute):
        self.MINUTE = minute
        self.QUARTER = minute * 15
        self.HALF_HOUR = minute * 30
        self.HOUR = minute * 60
        self.DAY = minute * 24


class SecondMeasure(TimeMeasure):
    """以秒为基础的计量.
    """

    def __init__(self):
        TimeMeasure.__init__(self, 60)


class MinuteMeasure(TimeMeasure):
    """以分钟为基础的计量.
    """

    def __init__(self):
        TimeMeasure.__init__(self, 1)


second_measure = SecondMeasure()
minute_measure = MinuteMeasure()

if __name__ == "__main__":
    print(SecondMeasure().MINUTE)
    print(MinuteMeasure().MINUTE)
