#!usr/bin/env python
# coding: utf-8

from tornado import gen
from tornado.log import app_log
from tornado.web import RequestHandler, asynchronous

from libs.upload.common import get_public_dl_url, get_shift_rs_url


class MainHandler(RequestHandler):
    def data_received(self, chunk):
        pass

    @asynchronous
    @gen.coroutine
    def get(self):
        self.write("Hello, world!")


class CommunalHandler(RequestHandler):
    def data_received(self, chunk):
        pass

    @asynchronous
    @gen.coroutine
    def get(self):
        file_info = self.get_argument("file")
        real_url = get_public_dl_url(file_info)
        app_log.info("public_download ==> %s" % real_url)
        return self.redirect(real_url)


class PrivatelyHandler(RequestHandler):
    def data_received(self, chunk):
        pass

    @asynchronous
    @gen.coroutine
    def get(self):
        file_info = self.get_argument("file")
        real_url = get_shift_rs_url(file_info)
        app_log.info("private_download ==> %s" % real_url)
        return self.redirect(real_url)
