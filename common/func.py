#!usr/bin/env python
# coding: utf-8

"""公共方法.
"""

from __future__ import unicode_literals, print_function

import os
import shutil
from xpinyin import Pinyin

pinyin = Pinyin()


def get_info_by_path(file_path):
    """根据文件存放结构获取信息.
    """

    dz_info = os.path.dirname(file_path).rsplit(os.sep, 2)[-2:]
    if len(dz_info) != 2:
        raise Exception("文件存放路径异常! 必须放在[plate%sauthor]之下!" % os.sep)

    suffix = os.path.splitext(file_path)[-1]
    suffix = suffix if suffix else ""
    return dz_info[0], dz_info[1], suffix


def get_plate_map_conf(plate_map_string):
    """转换从数据库导出的数据.

        SELECT fid, name FROM `bbs_forum_forum` WHERE status=1 AND type= 'forum';
    """

    dict_data = {}
    lines = plate_map_string.split("\n")
    for line in lines:
        key_value_list = line.strip(" ").strip("|").split("|")
        if len(key_value_list) < 2:
            continue
        dict_key = pinyin.get_pinyin(key_value_list[1]).lower()
        dict_data[dict_key] = int(key_value_list[0])

    print(dict_data)
    return dict_data


class FileProcess(object):
    """文件处理."""

    def __init__(self, path):
        """文件路径."""

        self.path = path

    def read(self):
        """读取."""

        if os.path.exists(self.path) and os.path.isfile(self.path):
            with open(self.path, 'rb') as f:
                lines = f.readall()
                return lines

    def move(self, new_path):
        """移动."""

        if not os.path.exists(self.path):
            raise IOError("Path Not Exist!")

        if not os.path.exists(new_path):
            os.makedirs(new_path)

        shutil.move(self.path, new_path)

    def copy(self, new_path):
        """移动."""

        if not os.path.exists(self.path):
            raise IOError("Path Not Exist!")

        if not os.path.exists(new_path):
            os.makedirs(new_path)

        # 复制文件
        if os.path.isfile(self.path):
            new_file = os.path.join(new_path, os.path.basename(self.path))
            shutil.copyfile(self.path, new_file)  # 参数A和B都只能是文件
        elif os.path.isdir(self.path):
            shutil.copy(self.path, new_path)  # 参数A只能是文件夹, 参数B可是文件或目标目录
        else:
            pass

    def remove(self):
        """删除."""

        if not os.path.exists(self.path):
            raise IOError("Path Not Exist!")

        if os.path.isfile(self.path):
            # 删除文件
            os.remove("file")
        elif os.path.isdir(self.path):
            # 删除目录
            # os.rmdir(self.path)  # 只能删除空目录
            shutil.rmtree(self.path)  # 空目录,有内容的目录都可以删
        else:
            pass


class FileFinished(object):
    """文件上传完成处理.

        移走放到其它目录, seek_dir ==> done_dir.
    """

    def __init__(self, seek_dir, done_dir):
        """seek_dir: 搜索目录; done_dir: 移到的目录."""

        self.seek_directory = seek_dir
        self.done_directory = done_dir

    def batch_move(self, entities_list):
        """批量移动文件列表."""

        def make_dirs(directory):
            if not os.path.exists(directory):
                os.makedirs(directory)

        make_dirs(self.done_directory)
        for entity in entities_list:
            dir_name = os.path.dirname(entity)
            new_path = dir_name.replace(self.seek_directory, self.done_directory)
            make_dirs(self.done_directory)
            shutil.move(entity, new_path)


if __name__ == "__main__":
    pass
