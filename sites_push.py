#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals, print_function

import json
import os
import sys
import traceback

from baidu.site_push import SitePush
from conf.data_config import forum_session
from conf.logger_config import broad_site_info
from models.remote import ForumThread

reload(sys)
sys.setdefaultencoding('utf-8')


def get_thread_entities():
    """规避使用'autoload'缺陷而刻意从类独立出.
    """

    thread_entities = None
    try:
        thread_entities = forum_session.query(ForumThread).all()
    except Exception, ex:
        print(ex)
        traceback.print_exc()
    finally:
        forum_session.close()

    return thread_entities


class BroadSite(SitePush):
    """宽语站点.
    """

    site = "www.ikuanyu.com"
    token = 'KG922tmSgsnuYsaq'

    def gen_data(self):
        """生成数据.
        """

        thread_entities = get_thread_entities()
        if thread_entities:
            site_url = "http://%s/thread-%s-1-1.html\n"
            threads_total = len(thread_entities)

            if os.path.exists('urls.txt'):
                os.remove('urls.txt')

            with open('urls.txt', 'ab') as f:
                for index, entity in enumerate(thread_entities):
                    entity = json.loads(str(entity))
                    f.write(site_url % (self.site, str(entity.get("tid"))))
                    broad_site_info.info("Info: Reach up to (%s / %s)" % (index, threads_total))


if __name__ == '__main__':
    """实例调度.
    """

    broad_site = BroadSite(BroadSite.site, BroadSite.token)
    broad_site.push_site()
