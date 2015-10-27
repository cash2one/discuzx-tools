#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

import os
from sevencow import Cow
from sevencow import CowException
from conf.store_config import ACCESS_KEY, BUCKET_NAME, SECRET_KEY

cow = Cow(ACCESS_KEY, SECRET_KEY)
bucket = cow.get_bucket(BUCKET_NAME)

directory = os.path.join(os.path.dirname(os.path.dirname(__file__)), "kylin_img")
files = os.listdir(directory)


def test_list_buckets():
    """列举所有buckets.
    """

    all_buckets = cow.list_buckets()
    print('all_buckets:', all_buckets)


def test_list_files():
    """列出一个bucket中的所有文件.
    """

    all_files = bucket.list_files()
    print('all_buckets:', all_files)


def test_actions(kind=None):
    """上传, 删除, 查看文件信息.
    """

    # 这三种是一类操作，因为只要提供文件名即可

    if kind == 1:
        bucket.put(files[0])  # 上传单个文件
        bucket.put(files[1], files[2], files[3])  # 批量上传

    if kind == 2:
        print(bucket.stat(os.path.basename(files[0])))  # 查看单个文件信息
        print(bucket.stat(os.path.basename(files[1]), os.path.basename(files[2]), os.path.basename(files[3])))  # 批量查看

    if kind == 3:
        bucket.delete(os.path.basename(files[0]))  # 删除单个文件
        bucket.delete(os.path.basename(files[1]), os.path.basename(files[2]), os.path.basename(files[3]))  # 批量删除


def test_upload():
    """
        默认情况下put上传是使用文件本身的名字作为上传后的名字(也就是在bucket中key).
        但你也可以给put方法加一个`names`关键字参数来指定文件上传后应该是什么名字.
    """

    test_actions(3)

    bucket.put(files[0], names={'test/s1': 's'})  # 本地文件'a'，上传后的在七牛中的名字是'x'
    bucket.put(files[1], files[2], files[3],
               names={files[1]: 'x', files[2]: 'y', files[3]: 'z'})  # 上传后，'b1','b2','b3'的名字分别为'x','y','z'

    bucket.put(files[1], files[2], files[3], names={files[3]: 'z'})  # 只改变'b3'的名字为'z'，'b1','b2'不变


def test_copy_move():
    """拷贝, 移动（改名）.
    """

    test_actions(1)

    # 这两个操作都需要提供源文件名和目标文件名
    bucket.copy(files[1], 's2')  # 将'a' 拷贝至'b'
    bucket.copy(('b1', 'a'), ('b2', 'b'), ('b3', 'c'))  # 批量拷贝
    bucket.move(files[1], 's')  # 将'a' 改名为'b'
    bucket.move(('b1', 'x'), ('b2', 'y'), ('b3', 'z'))  # 批量改名


def test_exc():
    u"""异常.
    """

    # 以上操作任何错误都会引发异常,只要请求api返回的不是200,所以安全的做法是这样：
    try:
        bucket.copy(('s1', 'b1'), ('c', 'd'))
    except CowException as e:
        print(e.url)  # 出错的url
        print(e.status_code)  # 返回码
        print(e.content)  # api 错误的原因


if __name__ == '__main__':
    u"""testing.
    """

    print("testing ...")

    # test_list_buckets()
    # test_list_files()
    # test_actions()
    # test_upload()
    # test_copy_move()
    # test_exc()
    pass
