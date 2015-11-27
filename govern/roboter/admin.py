#!/usr/bin/env python
# coding: utf-8

from django.contrib import admin
from django.contrib.auth import get_permission_codename
from models import BbsAttachment, BbsMember, BbsSurplus, BbsThread


class CustomModelAdmin(admin.ModelAdmin):
    def has_view_permission(self, request):
        opts = self.opts
        codename = get_permission_codename('read_only', opts)
        return request.user.has_perm("%s.%s" % (opts.app_label, codename))


class AttachmentAdmin(CustomModelAdmin):
    list_display = ('id', 'file_name', 'key_name', 'md5sum', 'plate', 'status',
                    'author', 'create_datetime', 'upload_datetime')

    ordering = ('-upload_datetime', '-create_datetime')
    search_fields = ('status', 'author')


class MemberAdmin(CustomModelAdmin):
    list_display = ('id', 'username', 'password', 'email', 'dz_uid', 'create_datetime')
    ordering = ('-create_datetime',)
    date_hierarchy = 'create_datetime'
    search_fields = ('username', 'dz_uid')


class SurplusAdmin(CustomModelAdmin):
    list_display = ('id', 'fid', 'path', 'md5sum', 'plate', 'author', 'create_datetime')
    ordering = ('-create_datetime',)
    date_hierarchy = 'create_datetime'
    search_fields = ('author', 'plate')


class ThreadAdmin(CustomModelAdmin):
    list_display = ('id', 'thread_id', 'post_id', 'attachment_id', 'robot_data_id', 'create_datetime')
    ordering = ('-create_datetime',)
    date_hierarchy = 'create_datetime'
    search_fields = ('thread_id', 'post_id', 'robot_data_id')


# admin.site.register(BbsAttachment)
# admin.site.register(BbsMember)
# admin.site.register(BbsSurplus)
# admin.site.register(BbsThread)

admin.site.register(BbsMember, MemberAdmin)
admin.site.register(BbsAttachment, AttachmentAdmin)
admin.site.register(BbsSurplus, SurplusAdmin)
admin.site.register(BbsThread, ThreadAdmin)
