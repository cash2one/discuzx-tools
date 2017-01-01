# !usr/bin/env python
# coding: utf-8

from __future__ import print_function, unicode_literals

import time

from splinter import Browser


def author_sure(browser, author):
    """身份认证.

        :parameter browser: 浏览器
        :parameter author: 身份信息
    """

    fill_data, btn_info = author.get('fill'), author.get('submit')

    for (key, value) in fill_data:
        browser.fill(key, value)

    button = None
    if btn_info[0].lower() == 'id':
        button = browser.find_by_id(btn_info[1])
    elif btn_info[0].lower() == 'name':
        button = browser.find_by_name(btn_info[1])

    if button:
        button.click()


def visited_quit(site_pages, stay=5, auth=False):
    """访问站点网页列表,访完关闭浏览器.

        :parameter site_pages: 网页列表
        :parameter auth: 是否需身份授权
        :parameter stay: 逗留秒数
    """

    with Browser() as browser:
        pages = site_pages.get("data")
        for i, page in enumerate(pages):
            browser.visit(str(page))
            if auth and not i:
                author = site_pages.get("auth")
                if author:
                    author_sure(browser, author)
            time.sleep(stay)


def visited_open(site_pages, stay=5, auth=False):
    """访问站点网页列表,访完保留浏览器,先快速浏览,最后页定位.

        :parameter site_pages: 网页列表
        :parameter auth: 是否需身份授权
        :parameter stay: 逗留秒数
    """

    browser = Browser()
    pages = site_pages.get("data")
    count = len(pages)
    for i, page in enumerate(pages):
        browser.visit(str(page))
        if auth and not i:
            author = site_pages.get("auth")
            if author:
                author_sure(browser, author)
        if i < count - 1:
            time.sleep(stay)
