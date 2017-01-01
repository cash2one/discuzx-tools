#!usr/bin/env python
# coding: utf-8

"""任务牵涉的数据模型.
"""

from __future__ import unicode_literals, print_function

from common.func import CacheService

from base import BaseModel
from conf.data_config import generate_db_models, robot_session
from libs.models import Member, Thread


class ModelFactory(object):
    """分表工厂.
    """

    @staticmethod
    def get_attachment(index=0):
        """获取映射到指定索引的分表.

            :parameter index 分表索引
        """

        try:
            forum_attachment = generate_db_models(
                'bbs_forum_attachment_%d' % index)

            class ForumAttachment(forum_attachment, BaseModel):
                def __init__(self, **kargs):
                    BaseModel.__init__(self, **kargs)
        except Exception as ex:
            print(ex)
        else:
            return ForumAttachment


def cache_thread_member():
    """从数据库载入数据(thread,member).
    """

    CacheService.cache_data_delete_model("forum_thread")
    CacheService.cache_data_delete_model("common_member")

    if not CacheService.cache_table_dict.get("forum_thread", False):
        forum_thread_entities = robot_session.query(Thread).all()
        CacheService.cache_data_import_model(
            forum_thread_entities, "forum_thread")

    if not CacheService.cache_table_dict.get("common_member", False):
        common_member_entities = robot_session.query(Member).all()
        CacheService.cache_data_import_model(
            common_member_entities, "common_member")
