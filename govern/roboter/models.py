#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

from django.db import models


class BbsAttachment(models.Model):
    id = models.IntegerField(primary_key=True)
    file_name = models.CharField(max_length=255)
    key_name = models.CharField(max_length=80, blank=True, null=True)
    down_link = models.CharField(max_length=150, blank=True, null=True)
    md5sum = models.CharField(max_length=80, blank=True, null=True)
    plate = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    author = models.CharField(max_length=45, blank=True, null=True)
    create_datetime = models.DateTimeField()
    upload_datetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bbs_attachment'


class BbsMember(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    dz_uid = models.IntegerField(blank=True, null=True)
    create_datetime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'bbs_member'


class BbsSurplus(models.Model):
    id = models.IntegerField(primary_key=True)
    fid = models.IntegerField(blank=True, null=True)
    path = models.CharField(max_length=255)
    md5sum = models.CharField(max_length=80, blank=True, null=True)
    plate = models.IntegerField(blank=True, null=True)
    author = models.CharField(max_length=45, blank=True, null=True)
    create_datetime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'bbs_surplus'


class BbsThread(models.Model):
    id = models.IntegerField(primary_key=True)
    thread_id = models.IntegerField()
    post_id = models.IntegerField()
    attachment_id = models.IntegerField(blank=True, null=True)
    robot_data_id = models.IntegerField(blank=True, null=True)
    create_datetime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'bbs_thread'
