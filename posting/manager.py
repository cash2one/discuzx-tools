#!usr/bin/env python
# coding: utf-8

"""发信息相关的操作.
"""

from __future__ import unicode_literals, print_function

import sys
import time
import traceback

from sqlalchemy.sql import text

from conf.data_config import forum_session, forum_engine
from conf.logger_config import post_info
from models.remote import ForumPost, ForumThread, ForumAffixIndex
from models.submeter import ModelFactory
from posting import type_attachment, attachment_enable, download_link

reload(sys)
sys.setdefaultencoding('utf8')


def alchemy_sql(sql, kind="list"):
    """执行SQL语句.

        :parameter sql 可执行SQL语句
        :parameter kind: ["list","first","scalar","execute"]
    """

    result = None
    sql = text(sql)
    kind = kind.lower()
    conn = forum_engine.connect()

    try:
        if kind == "list":
            result = conn.execute(sql).fetchall()
        elif kind == "first":
            result = conn.execute(sql).first()
        elif kind == "scalar":
            result = conn.execute(sql).scalar()
        elif kind == "execute":
            result = conn.execute(sql)
    except Exception, ex:
        print(ex)
        raise ex
    finally:
        conn.close()

    return result


def spread_repair_post(check=False):
    """帖子pid自增键.

        警告: 特殊危险, 请不要轻易运行, 除非你理解可能产生的风险.
        :parameter check: 防止错误调用运行增加参数做安全阀.
    """

    if check:
        alchemy_sql("INSERT INTO bbs_forum_post_tableid() VALUES();", kind="execute")
    else:
        max_pid = alchemy_sql("select max(pid) from bbs_forum_post_tableid;", "scalar")
        return max_pid


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


def spread_post(uid, tid, fid, username, message):
    """只适用于回帖子.

        :parameter uid      会员Id
        :parameter fid      论坛Id
        :parameter tid      主题Id
        :parameter username 会员名称
        :parameter message  内容
    """

    pid = 0

    try:
        max_pid = spread_repair_post()

        forum_post = ForumPost(
            __pid=max_pid + 1,
            __tid=tid,
            __fid=fid,
            __message=message,
            __author=username,
            __authorid=uid,
            __usesig=1,
            __dateline=int(time.time()))

        ForumPost.add(forum_post)
    except Exception, ex:
        print(ex)
        # raise ex
    else:
        spread_repair_post(True)
        pid = forum_post.__pid

    return pid


def spread_info(subject, message, author, fid, tid=0, file_name=None, attachment=None):
    """发信息.

        :parameter subject  标题
        :parameter message  内容
        :parameter author   会员名
        :parameter fid      论坛Id
        :parameter tid      主题Id
        :parameter file_name
        :parameter attachment
    """

    aid = 0  # 使用DZ远程附件时附件Id
    refresh = True

    if not attachment_enable:
        message = ''.join((message, download_link % (attachment, file_name)))

    try:
        # 处理 Data too long for column 'subject'错误
        subject_count = len(subject)
        if subject_count > 80:
            subject = subject[:80]

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
                __attachment=type_attachment,  # 附件,0无附件 1普通附件 2有图片附件
                # __status=0,
            )

            forum_session.add(forum_thread)
            if refresh:
                forum_session.flush()
                forum_session.refresh(forum_thread)
            tid = forum_thread.__tid
        post_info.info("1: 发主题 ==>> (%s)" % str(tid))

        # 2:发帖子
        max_pid = spread_repair_post()

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
            __attachment=type_attachment,
            __dateline=int(time.time()),
        )

        forum_session.add(forum_post)
        if refresh:
            forum_session.flush()
            forum_session.refresh(forum_post)
        pid = forum_post.__pid
        post_info.info("2: 发帖子 ==>> (%s)" % str(pid))

        if attachment_enable:
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
            post_info.info("3: 发附件 ==>> (%s)" % str(aid))

        forum_session.commit()
    except Exception, ex:
        traceback.print_exc()
        forum_session.rollback()
        raise ex
    else:
        spread_repair_post(True)
    finally:
        forum_session.close()

    return tid, pid, aid
