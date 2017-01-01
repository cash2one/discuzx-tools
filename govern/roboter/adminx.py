#!/usr/bin/env python
# coding: utf-8

import xadmin
from xadmin import views
from xadmin.plugins.batch import BatchChangeAction

from .models import BbsAttachment, BbsMember, BbsSurplus, BbsThread, BbsPost


class MainDashboard(object):
    widgets = [
        [{"type": "html", "title": "Test Widget",
          "content": "<h3> Welcome to ikuanyu.com! </h3>"}, ],
        [{"type": "qbutton", "title": "Quick Start",
          "btns": [{'model': BbsAttachment}, {'model': BbsMember}, ]}, ]
    ]


xadmin.site.register(views.website.IndexView, MainDashboard)


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


xadmin.site.register(views.BaseAdminView, BaseSetting)


class GlobalSetting(object):
    global_search_models = [BbsAttachment, BbsMember]
    global_models_icon = {
        BbsAttachment: 'fa fa-laptop', BbsMember: 'fa fa-cloud'
    }
    menu_style = 'default'  # 'accordion'


xadmin.site.register(views.CommAdminView, GlobalSetting)


class ThreadInline(object):
    model = BbsThread
    extra = 1
    style = 'accordion'


class MemberXAdmin(object):
    list_display = ('id', 'username', 'password',
                    'email', 'dz_uid', 'create_datetime')
    search_fields = ['username', 'email', 'dzuid']
    relfield_style = 'fk-ajax'
    reversion_enable = True

    actions = [BatchChangeAction, ]
    batch_fields = ('dz_uid', 'create_datetime')


class AttachmentXAdmin(object):
    list_display = ('id', 'file_name', 'key_name', 'md5sum', 'plate',
                    'status', 'author', 'create_datetime', 'upload_datetime')

    list_filter = ['author', 'file_name']
    search_fields = ['status', 'author', 'file_name']
    style_fields = {'hosts': 'checkbox-inline'}


class ThreadXAdmin(object):
    list_display = (
        'id', 'thread_id', 'post_id', 'attachment_id', 'robot_data_id',
        'create_datetime')
    list_display_links = ('robot_data_id',)

    search_fields = ['thread_id', 'post_id', 'robot_data_id']
    style_fields = {'hosts': 'checkbox-inline'}


class PostXAdmin(object):
    list_display = ('id', 'uid', 'tid', 'pid', 'fid', 'create_datetime')
    search_fields = ['uid', 'tid', 'fid']
    style_fields = {'hosts': 'checkbox-inline'}


class BbsPostContentXAdmin(object):
    list_display = (
        'id', 'content', 'status', 'user', 'update_datetime',
        'create_datetime')
    search_fields = ['user', 'status', 'update_datetime']
    style_fields = {'hosts': 'checkbox-inline'}


class SurplusXAdmin(object):
    list_display = (
        'id', 'fid', 'path', 'md5sum', 'plate', 'author', 'create_datetime')
    list_display_links = ('fid',)

    list_filter = ['fid', 'author', 'plate']
    search_fields = ['author', 'plate']
    reversion_enable = True


xadmin.site.register(BbsMember, MemberXAdmin)
xadmin.site.register(BbsAttachment, AttachmentXAdmin)
xadmin.site.register(BbsSurplus, SurplusXAdmin)
xadmin.site.register(BbsThread, ThreadXAdmin)
xadmin.site.register(BbsPost, PostXAdmin)
xadmin.site.register(BbsPost, PostXAdmin)
