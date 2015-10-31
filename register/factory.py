#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""模拟用户数据.
"""

from __future__ import unicode_literals, print_function

from faker import Factory
from testdata import DictFactory, RandomInteger, RandomLengthStringFactory, FakeDataFactory
from common.common import ChinaProvider
from control import SWITCH_ZH_CN

if SWITCH_ZH_CN:
    china_factory = Factory.create('zh_CN')
    china_factory.add_provider(ChinaProvider)
    FakeDataFactory._FAKER_FACTORY = china_factory

    cn_bio = FakeDataFactory('cn_bio')
    cn_tag = FakeDataFactory('cn_tag')
    cn_email = FakeDataFactory('cn_email')
    cn_message = FakeDataFactory('cn_message')
else:
    cn_bio = cn_tag = RandomLengthStringFactory(min_chars=5, max_chars=30)
    cn_message = cn_email = RandomLengthStringFactory(min_chars=5, max_chars=30)


class FakeMember(DictFactory):
    username = RandomLengthStringFactory(4, 10)
    password = RandomLengthStringFactory(6, 20)
    assist_number = RandomInteger(10**2, 10**15)
    email = cn_email


class FakePost(DictFactory):
    bio = cn_bio
    tag = cn_tag
    message = cn_message
