# !usr/bin/env python
# coding: utf-8

from __future__ import print_function, unicode_literals

from conf.data_splinter import sites_pages

from libs.common.accessor import visited_quit

if __name__ == '__main__':
    visited_quit(sites_pages, auth=True)
