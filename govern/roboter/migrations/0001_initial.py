# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BbsAttachment',
            fields=[
                ('id', models.IntegerField(
                    serialize=False,
                    verbose_name='id',
                    primary_key=True)),
                ('file_name',
                 models.CharField(max_length=255, verbose_name='file name')),
                ('key_name', models.CharField(
                    max_length=80,
                    null=True,
                    verbose_name='key name',
                    blank=True)),
                ('down_link', models.CharField(
                    max_length=150,
                    null=True,
                    verbose_name='down link',
                    blank=True)),
                ('md5sum', models.CharField(
                    max_length=80,
                    null=True,
                    verbose_name='md5sum',
                    blank=True)),
                ('plate', models.IntegerField(
                    null=True,
                    verbose_name='plate',
                    blank=True)),
                ('status',
                 models.IntegerField(
                     null=True,
                     verbose_name='status',
                     blank=True)),
                ('author', models.CharField(
                    max_length=45,
                    null=True,
                    verbose_name='author',
                    blank=True)),
                ('create_datetime',
                 models.DateTimeField(verbose_name='create datetime')),
                ('upload_datetime', models.DateTimeField(
                    null=True,
                    verbose_name='upload datetime',
                    blank=True)),
            ],
            options={
                'verbose_name': 'bbs attachment',
                'db_table': 'bbs_attachment',
                'managed': False,
                'verbose_name_plural': 'bbs attachment list',
                'permissions': (('read_only', 'Can read only'),),
            },
        ),
        migrations.CreateModel(
            name='BbsMember',
            fields=[
                ('id', models.IntegerField(
                    serialize=False,
                    verbose_name='id',
                    primary_key=True)),
                ('username',
                 models.CharField(max_length=45, verbose_name='username')),
                ('password',
                 models.CharField(max_length=45, verbose_name='password')),
                ('email',
                 models.CharField(max_length=45, verbose_name='email')),
                ('dz_uid',
                 models.IntegerField(
                     null=True,
                     verbose_name='dz uid',
                     blank=True)),
                ('create_datetime',
                 models.DateTimeField(verbose_name='create datetime')),
            ],
            options={
                'verbose_name': 'bbs member',
                'db_table': 'bbs_member',
                'managed': False,
                'verbose_name_plural': 'bbs member list',
                'permissions': (('read_only', 'Can read only'),),
            },
        ),
        migrations.CreateModel(
            name='BbsSurplus',
            fields=[
                ('id', models.IntegerField(
                    serialize=False,
                    verbose_name='id',
                    primary_key=True)),
                ('fid', models.IntegerField(
                    null=True,
                    verbose_name='fid',
                    blank=True)),
                (
                    'path',
                    models.CharField(max_length=255, verbose_name='path')),
                ('md5sum', models.CharField(
                    max_length=80,
                    null=True,
                    verbose_name='md5sum',
                    blank=True)),
                ('plate', models.IntegerField(
                    null=True,
                    verbose_name='plate',
                    blank=True)),
                ('author', models.CharField(
                    max_length=45,
                    null=True,
                    verbose_name='author',
                    blank=True)),
                ('create_datetime',
                 models.DateTimeField(verbose_name='create datetime')),
            ],
            options={
                'verbose_name': 'bbs surplus',
                'db_table': 'bbs_surplus',
                'managed': False,
                'verbose_name_plural': 'bbs surplus list',
                'permissions': (('read_only', 'Can read only'),),
            },
        ),
        migrations.CreateModel(
            name='BbsThread',
            fields=[
                ('id', models.IntegerField(
                    serialize=False,
                    verbose_name='id',
                    primary_key=True)),
                ('thread_id', models.IntegerField(verbose_name='thread id')),
                ('post_id', models.IntegerField(verbose_name='post id')),
                ('attachment_id',
                 models.IntegerField(
                     null=True,
                     verbose_name='attachment id',
                     blank=True)),
                ('robot_data_id',
                 models.IntegerField(
                     null=True,
                     verbose_name='robot data id',
                     blank=True)),
                ('create_datetime',
                 models.DateTimeField(verbose_name='create datetime')),
            ],
            options={
                'verbose_name': 'bbs thread',
                'db_table': 'bbs_thread',
                'managed': False,
                'verbose_name_plural': 'bbs thread list',
                'permissions': (('read_only', 'Can read only'),),
            },
        ),
    ]
