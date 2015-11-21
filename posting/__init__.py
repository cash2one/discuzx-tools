#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 是否使用DZ远程附件形式
attachment_enable = False

# 附件: 0无附件; 1普通附件; 2有图片附件
type_attachment = 1 if attachment_enable else 0

# DZ内置下载链接格式
download_link = '\r\n[url=http://file.ikuanyu.com/source/private/download?file=%s]%s[/url]'
