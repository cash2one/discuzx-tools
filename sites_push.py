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
from conf.env_conf import dz_site, dz_push_token

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

    site = dz_site
    token = dz_push_token
    urls_size = 500

    def gen_data(self):
        """生成数据.
        """

        thread_entities = get_thread_entities()
        if thread_entities:
            site_url = "http://%s/thread-%s-1-1.html\n"
            threads_total = len(thread_entities)

            # data_splinter:生成访问配置数据
            current_dir = os.path.join(os.path.dirname(__file__), 'conf')
            gen_file = os.path.join(current_dir, 'data_splinter.py')
            if os.path.exists(gen_file):
                os.remove(gen_file)

            pages_list = []
            data_robots = open(gen_file, 'wb')
            site_format = "        'http://%s/thread-%s-1-1.html',"
            tpl_content = open(os.path.join(current_dir, 'data_splinter.tpl'), 'rb').read()

            urls_file = {}
            times = int(threads_total / self.urls_size) + 1
            for index in xrange(0, times):
                urls = 'urls_%d.txt' % index
                if os.path.exists(urls):
                    os.remove(urls)

                self._urls_list.append(urls)
                urls_file[index] = open(urls, 'ab')

            for index, entity in enumerate(thread_entities):
                entity = json.loads(str(entity))
                current_index = int(index / self.urls_size)
                urls_file[current_index].write(site_url % (self.site, str(entity.get("tid"))))
                broad_site_info.info("Info: Reach up to (%s / %s)" % (index, threads_total))
                pages_list.append(site_format % (self.site, str(entity.get("tid"))))

            # data_splinter:写入配置数据
            data_robots.write(str(tpl_content % '\n'.join(pages_list)))
            data_robots.close()

            for index in xrange(0, times):
                urls_file[index].close()


if __name__ == '__main__':
    """实例调度.
    """

    # 仅仅生成数据
    only_gen_data = True

    broad_site = BroadSite(BroadSite.site, BroadSite.token)
    if only_gen_data:
        broad_site.gen_data()
    else:
        broad_site.push_site()
