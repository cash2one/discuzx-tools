# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('roboter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BbsPost',
            fields=[
                ('id', models.IntegerField(serialize=False, verbose_name='id', primary_key=True)),
                ('uid', models.IntegerField(verbose_name='thread id')),
                ('tid', models.IntegerField(verbose_name='thread id')),
                ('pid', models.IntegerField(verbose_name='post id')),
                ('fid', models.IntegerField(verbose_name='plate id')),
                ('create_datetime', models.DateTimeField(verbose_name='create datetime')),
            ],
            options={
                'verbose_name': 'bbs post',
                'db_table': 'bbs_post',
                'managed': False,
                'verbose_name_plural': 'bbs post list',
                'permissions': (('read_only', 'Can read only'),),
            },
        ),
        migrations.CreateModel(
            name='BbsPostContent',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='id', primary_key=True)),
                ('content', models.CharField(max_length=800, verbose_name='content')),
                ('status', models.IntegerField(verbose_name='status')),
                ('update_datetime', models.DateTimeField(auto_now=True, verbose_name='update datetime')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='create datetime')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'bbs_post_content',
                'verbose_name': 'bbs post content',
                'verbose_name_plural': 'bbs post content list',
                'permissions': (('read_only', 'Can read only'),),
            },
        ),
    ]
