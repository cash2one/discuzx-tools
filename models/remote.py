#!usr/bin/env python
# coding: utf-8

"""任务牵涉的数据模型.
"""

from __future__ import unicode_literals, print_function
from conf.data_config import generate_db_models
from base import BaseModel

common_member = generate_db_models('bbs_common_member')
forum_thread = generate_db_models('bbs_forum_thread')
forum_post = generate_db_models('bbs_forum_post')

forum_attachment_index = generate_db_models('bbs_forum_attachment')
forum_attachment_content = generate_db_models('bbs_forum_attachment_0')


class CommonMember(common_member, BaseModel):
    def __init__(self, **kargs):
        BaseModel.__init__(self, **kargs)


class ForumThread(forum_thread, BaseModel):
    def __init__(self, **kargs):
        BaseModel.__init__(self, **kargs)


class ForumPost(forum_post, BaseModel):
    def __init__(self, **kargs):
        BaseModel.__init__(self, **kargs)


class ForumAttachmentIndex(forum_attachment_index, BaseModel):
    def __init__(self, **kargs):
        BaseModel.__init__(self, **kargs)


class ForumAttachment(forum_attachment_content, BaseModel):
    def __init__(self, **kargs):
        BaseModel.__init__(self, **kargs)
