#!usr/bin/env python
# coding: utf-8

from tornado import gen
from tornado.web import RequestHandler, asynchronous
from upload.common import get_public_dl_url, get_shift_rs_url


class CommunalHandler(RequestHandler):
    @asynchronous
    @gen.coroutine
    def get(self):
        file_info = self.get_argument("file")
        new_url = get_public_dl_url(file_info)
        print new_url
        return self.redirect(new_url)


class PrivatelyHandler(RequestHandler):
    @asynchronous
    @gen.coroutine
    def get(self):
        file_info = self.get_argument("file")
        new_url = get_shift_rs_url(file_info)
        print new_url
        return self.redirect(get_shift_rs_url(file_info))
