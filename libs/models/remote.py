#!usr/bin/env python
# coding: utf-8

"""任务牵涉的数据模型.
"""

from __future__ import unicode_literals, print_function
from conf.data_config import generate_db_models
from base import BaseModel

common_member = generate_db_models('bbs_common_member')
center_member = generate_db_models('bbs_ucenter_members')
common_member_status = generate_db_models('bbs_common_member_status')

forum_post = generate_db_models('bbs_forum_post')
forum_thread = generate_db_models('bbs_forum_thread')
forum_affix_index = generate_db_models('bbs_forum_attachment')
forum_member_recommend = generate_db_models('bbs_forum_memberrecommend')


class CommonMember(common_member, BaseModel):
    def __init__(self, **kargs):
        BaseModel.__init__(self, **kargs)


class CommonMemberStatus(common_member_status, BaseModel):
    def __init__(self, **kargs):
        BaseModel.__init__(self, **kargs)


class CenterMember(center_member, BaseModel):
    def __init__(self, **kargs):
        BaseModel.__init__(self, **kargs)


class ForumThread(forum_thread, BaseModel):
    def __init__(self, **kargs):
        BaseModel.__init__(self, **kargs)


class ForumPost(forum_post, BaseModel):
    def __init__(self, **kargs):
        BaseModel.__init__(self, **kargs)


class ForumAffixIndex(forum_affix_index, BaseModel):
    def __init__(self, **kargs):
        BaseModel.__init__(self, **kargs)


class ForumMemberRecommend(forum_member_recommend, BaseModel):
    def __init__(self, **kargs):
        BaseModel.__init__(self, **kargs)
