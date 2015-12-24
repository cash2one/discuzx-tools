#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals, print_function

import os


class SitePush(object):
    """百度网址链接推送.
    """

    def __init__(self, site, token, kind=None):
        self._site = site
        self._token = token
        self._type = kind if kind else 'original'

    def _get_push_api(self):
        push_api = "http://data.zz.baidu.com/urls?site=%s&token=%s&type=%s"
        return push_api % (self._site, self._token, self._type)

    def gen_data(self):
        """生成数据.
        """
        pass

    def push_site(self):
        """主动推送数据.
        """

        self.gen_data()
        os.system("curl -H 'Content-Type:text/plain' --data-binary @urls.txt %s" % self._get_push_api())
