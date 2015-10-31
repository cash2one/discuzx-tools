#!usr/bin/env python
# coding: utf-8

import sys
import os

import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.autoreload
from tornado.log import app_log
from web.utils.options_parse import options, parse_options_config
from web.handler.views import CommunalHandler, PrivatelyHandler

reload(sys)
sys.setdefaultencoding("utf8")


def build_settings(**kargs):
    settings = dict()
    settings.update(**kargs)
    return settings


def show(handlers, url_width, handler_width):
    app_log.info("=" * int(url_width + handler_width))
    app_log.info("%-*s%-*s" % (url_width, "URL", handler_width, "HANDLER"))
    app_log.info("=" * int(url_width + handler_width))
    for url, _ in handlers:
        app_log.info("%-*s%-*s" % (url_width, url, handler_width, _))
    app_log.info("=" * int(url_width + handler_width))


def main():
    parse_options_config(os.path.join(os.path.dirname(__file__), "conf"))

    handlers = [
        (r"/download/file/public", CommunalHandler),
        (r"/download/file/private", PrivatelyHandler),
    ]

    show(handlers, 40, 60)
    settings = build_settings(**options.as_dict())
    application = tornado.web.Application(handlers, **settings)
    http_server = tornado.httpserver.HTTPServer(application, xheaders=True)
    http_server.listen(options.port)

    config_evn = settings.get("config").split(".")[-1].lower()
    if settings.get("debug") or config_evn == "debug":
        # 检测py文件的变动, 自动reload新的代码, 无需重启服务器.
        # 仅用于开发和测试阶段, 否则每次修改都重启Tornado服务.
        instance = tornado.ioloop.IOLoop.instance()
        tornado.autoreload.start(instance)
        instance.start()
    else:
        tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
