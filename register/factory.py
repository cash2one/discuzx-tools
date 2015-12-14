#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""模拟用户数据.
"""

from __future__ import unicode_literals, print_function

from faker import Factory
from testdata import DictFactory, RandomInteger, RandomLengthStringFactory, FakeDataFactory
from testdata.extra.mongodb import FieldFromCollection

from common.common import ChinaProvider
from control import SWITCH_ZH_CN
from conf.data_config import cache_option

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
    assist_number = RandomInteger(10 ** 2, 10 ** 15)
    email = cn_email


class FakeMemberStatus(DictFactory):
    reg_ip = FakeDataFactory('ipv4')
    last_ip = FakeDataFactory('ipv4')


class FakeRecommend(DictFactory):
    tid = FieldFromCollection(collection='forum_thread', field_name='thread_id', **cache_option)
    uid = FieldFromCollection(collection='common_member', field_name='dz_uid', **cache_option)
    opinion = RandomInteger(0, 100)


class FakePost(DictFactory):
    uid = FieldFromCollection(collection='common_member', field_name='dz_uid', **cache_option)
    tid = FieldFromCollection(collection='forum_thread', field_name='thread_id', **cache_option)
    fid = FieldFromCollection(collection='forum_thread', field_name='plate_id', **cache_option)
    username = FieldFromCollection(collection='common_member', field_name='username', **cache_option)
    # message = FieldFromCollection(collection='', field_name='', **cache_option)
    message = cn_message
