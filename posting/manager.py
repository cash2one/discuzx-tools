#!usr/bin/env python
# coding: utf-8

"""发信息相关的操作.
"""

from __future__ import unicode_literals, print_function

import time
from sqlalchemy.sql import text
from conf.data_config import forum_session, forum_engine
from models.submeter import ModelFactory
from models.remote import ForumPost, ForumThread, ForumAffixIndex


def alchemy_sql(sql, kind="list"):
    """执行SQL语句.

        :parameter kind: ["list","first","scalar"]
    """

    sql = text(sql)
    kind = kind.lower()
    conn = forum_engine.connect()

    if kind == "list":
        result = conn.execute(sql).fetchall()
    elif kind == "first":
        result = conn.execute(sql).first()
    elif kind == "scalar":
        result = conn.execute(sql).scalar()
    else:
        result = None

    return result


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


def spread_post(subject, message, author, fid, tid):
    """发帖子.

        :parameter subject  标题
        :parameter message  内容
        :parameter author   会员名
        :parameter fid      论坛Id
        :parameter tid      主题Id
    """

    try:
        max_pid = alchemy_sql("select max(pid) from bbs_forum_post;", "scalar")
        forum_post = ForumPost(
            __pid=max_pid + 1,
            __tid=tid,
            __fid=fid,
            __subject=subject,
            __message=message,
            __author=author[1],
            __authorid=author[0])

        ForumPost.add(forum_post)
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

    refresh = True

    try:
        if not tid:
            # 1: 发主题
            dateline = int(time.time())
            forum_thread = ForumThread(
                __fid=fid,
                __author=author[1],
                __authorid=author[0],
                __subject=subject,
                __dateline=dateline,
                __lastpost=dateline,
                __lastposter=author[1],
                __attachment=1,  # 附件,0无附件 1普通附件 2有图片附件
                # __status=0,
            )

            forum_session.add(forum_thread)
            if refresh:
                forum_session.flush()
                forum_session.refresh(forum_thread)
            tid = forum_thread.__tid
        print("1: 发主题 ==>> (%s)" % tid)

        # 2:发帖子
        max_pid = alchemy_sql("select max(pid) from bbs_forum_post;", "scalar")

        forum_post = ForumPost(
            __pid=max_pid + 1,
            __tid=tid,
            __fid=fid,
            __subject=subject,
            __message=message,
            __author=author[1],
            __authorid=author[0],
            __first=1,  # 是否是首贴
            __usesig=1,
            __attachment=1,
            __dateline=int(time.time()),

        )

        forum_session.add(forum_post)
        if refresh:
            forum_session.flush()
            forum_session.refresh(forum_post)
        pid = forum_post.__pid
        print("2: 发帖子 ==>> (%s)" % pid)

        # 3: 发附件
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
            __price=0,  # 附件价格
        )

        forum_session.add(forum_attachment)
        if refresh:
            forum_session.flush()
            forum_session.refresh(forum_attachment)
        aid = forum_attachment.__aid
        print("3: 发附件 ==>> (%s)" % aid)

        forum_session.commit()
    except Exception, ex:
        print(ex)
        forum_session.rollback()
        raise ex
    finally:
        forum_session.close()

    return tid, pid, aid
