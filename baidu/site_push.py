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
        self._urls_list = []

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
        if self._urls_list:
            push_api = self._get_push_api()
            command_format = (
                "curl -H 'Content-Type:text/plain'"
                " --data-binary @%s %s")

            for urls in self._urls_list:
                str_command = command_format % (urls, push_api)
                print(str_command)
                os.system(str_command)
