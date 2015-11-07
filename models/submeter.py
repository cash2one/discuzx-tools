#!usr/bin/env python
# coding: utf-8

"""任务牵涉的数据模型.
"""

from __future__ import unicode_literals, print_function
from conf.data_config import generate_db_models
from base import BaseModel


class ModelFactory(object):
    """分表工厂.
    """

    @staticmethod
    def get_attachment(index=0):
        """获取映射到指定索引的分表.

            :parameter index 分表索引
        """

        try:
            forum_attachment = generate_db_models('bbs_forum_attachment_%d' % index)

            class ForumAttachment(forum_attachment, BaseModel):
                def __init__(self, **kargs):
                    BaseModel.__init__(self, **kargs)
        except Exception, ex:
            print(ex)
        else:
            return ForumAttachment
