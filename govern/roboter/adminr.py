#!/usr/bin/env python
# coding: utf-8

import django_databrowse

from .models import (BbsAttachment, BbsMember, BbsSurplus,
                     BbsThread, BbsPost, BbsPostContent)

django_databrowse.site.register(BbsAttachment)
django_databrowse.site.register(BbsMember)
django_databrowse.site.register(BbsSurplus)
django_databrowse.site.register(BbsThread)
django_databrowse.site.register(BbsPost)
django_databrowse.site.register(BbsPostContent)
