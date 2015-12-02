#!usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals, print_function

from sqlalchemy import Column, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ForumMemberRecommend(Base):
    __tablename__ = "bbs_forum_memberrecommend"

    tid = Column(INTEGER)
    recommenduid = Column(INTEGER)
    dateline = Column(INTEGER)
