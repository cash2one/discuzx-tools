#!usr/bin/env python
# coding: utf-8

"""发信息相关的操作.
"""

from __future__ import unicode_literals, print_function

import time
from models.submeter import ModelFactory
from models.remote import ForumPost, ForumThread, ForumAffixIndex


def spread_attachment(tid, pid, author, file_name, attachment):
    """发附件操作.

        :parameter tid          主题id
        :parameter pid          帖子id
        :parameter author       会员

        :parameter file_name    原文件名
        :parameter attachment   系统生成路径名称
    """

    try:
        uid = author[0]
        index = int(str(tid)[-1])

        # 附件索引
        forum_affix_index = ForumAffixIndex(
            __tid=tid,
            __pid=pid,
            __uid=uid,
            __tableid=index)
        ForumAffixIndex.add(forum_affix_index)
        aid = forum_affix_index.__aid

        # 附件集合
        description = file_name.split(".")[0]
        attachment_class = ModelFactory.get_attachment(index)
        forum_attachment = attachment_class(
            __aid=aid,
            __tid=tid,
            __pid=pid,
            __uid=uid,
            __filename=file_name,
            __attachment=attachment,
            __description=description,
            __dateline=int(time.time()),
            __remote=1,  # 是否远程附件
            __price=2,  # 附件价格

            # 以下待扩展
            # __isimage=0,  # 是否图片
            # __width=0,  # 附件宽度
            # __thumb=0,  # 是否缩略图
            # __filesize=0,  # 文件大小
            # __readperm=0,  # 阅读权限
        )

        attachment_class.add(forum_attachment)
    except Exception, ex:
        print(ex)
    else:
        return forum_attachment.__aid


def spread_thread(subject, author, fid):
    """发主题.

        :parameter subject  标题
        :parameter author   会员名
        :parameter fid      论坛Id
    """

    try:
        forum_thread = ForumThread(
            __fid=fid,
            __author=author[1],
            __authorid=author[0],
            __subject=subject,
            __dateline=int(time.time()),
        )

        ForumThread.add(forum_thread)
    except Exception, ex:
        print(ex)
        return 0
    else:
        return forum_thread.__tid


def spread_post(subject, message, author, fid, tid):
    """发帖子.

        :parameter subject  标题
        :parameter message  内容
        :parameter author   会员名
        :parameter fid      论坛Id
        :parameter tid      主题Id
    """

    try:
        forum_post = ForumPost(
            __tid=tid,
            __fid=fid,
            __subject=subject,
            __message=message,
            __author=author[1],
            __authorid=author[0])

        ForumPost.add(forum_post)

        # 更新主题信息
        # lastpost 最后发表时间
        # lastposter 最后发表人
    except Exception, ex:
        print(ex)
        return 0
    else:
        return forum_post.__pid


def spread_info(subject, message, author, fid, tid=0, file_name=None, attachment=None):
    """发信息.

        :parameter subject  标题
        :parameter message  内容
        :parameter author   会员名
        :parameter fid      论坛Id
        :parameter tid      主题Id
    """

    try:
        if not tid:
            tid = spread_thread(subject, author, fid)

        pid = spread_post(subject, message, author, fid, tid)
        aid = spread_attachment(tid, pid, author, file_name, attachment) if file_name and attachment else 0
    except Exception, ex:
        print(ex)
        return 0, 0, 0
    else:
        return tid, pid, aid
