#!usr/bin/env python
# coding: utf-8

"""公共方法.
"""

from __future__ import unicode_literals, print_function

import os
import shutil


class FileProcess(object):
    """文件处理."""

    def __init__(self, path):
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


if __name__ == "__main__":
    pass
