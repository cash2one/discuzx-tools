#!/usr/bin/env python
# coding: utf-8

from django.contrib import admin

from models import BbsAttachment, BbsMember, BbsSurplus, BbsThread

admin.site.register(BbsAttachment)
admin.site.register(BbsMember)
admin.site.register(BbsSurplus)
admin.site.register(BbsThread)
