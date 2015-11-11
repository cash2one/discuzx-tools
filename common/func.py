#!usr/bin/env python
# coding: utf-8

"""公共方法.
"""

from __future__ import unicode_literals, print_function

import os
import hashlib
import shutil
import redis

from xpinyin import Pinyin
from conf.data_config import REDIS_CONFIG
from conf.logger_config import redis_data_log

pinyin = Pinyin()
redis_pool = redis.ConnectionPool(host=REDIS_CONFIG.get("redis_host"), port=REDIS_CONFIG.get("redis_port"))


class RedisService(object):
    def __init__(self, db=0, password=None):
        try:
            self._redis_cli = redis.Redis(connection_pool=redis_pool, db=db, password=password)
        except Exception, ex:
            self._redis_cli = None
            redis_data_log.error("redis连接失败：%s" % (str(ex)))

    def get(self, key):
        return self._redis_cli and self._redis_cli.get(key)

    def set(self, key, value):
        return self._redis_cli and self._redis_cli.set(key, value)

    def mset(self, **kwargs):
        return self._redis_cli and self._redis_cli.mset(**kwargs)

    def hget(self, name, key):
        return self._redis_cli and self._redis_cli.hget(name, key)


class Utils(object):
    @staticmethod
    def md5(text):
        """php内置md5加密一致.

            :parameter text
        """

        m = hashlib.md5(text).hexdigest()
        return m

    @staticmethod
    def dz_uc_md5(password, salt):
        """dz uc加密规则.

            :parameter password
            :parameter salt
        """

        return Utils.md5(''.join((Utils.md5(password), salt)))

    @staticmethod
    def md5sum(file_path):
        """计算文件的MD5值.

            :parameter file_path
        """

        try:
            with open(file_path, "rb") as f:
                return Utils.md5(f.read())
        except Exception, ex:
            print(ex)
            return ""

    @staticmethod
    def md5sum_bigfile(file_path):
        """计算文件的MD5值.

            :parameter file_path
        """

        def read_chunks(_fh):
            fh.seek(0)
            _chunk = fh.read(8096)
            while _chunk:
                yield _chunk
                _chunk = _fh.read(8096)
            else:
                # 最后要将游标放回文件开头
                _fh.seek(0)

        m = hashlib.md5()
        if isinstance(file_path, basestring) and os.path.exists(file_path):
            with open(file_path, "rb") as fh:
                for chunk in read_chunks(fh):
                    m.update(chunk)
        else:
            return ""
        return m.hexdigest()

    @staticmethod
    def get_info_by_path(file_path):
        """根据文件存放结构获取信息.

            :parameter file_path
            :return auth, plate, suffix: 作者, 版块, 后缀.
        """

        dz_info = os.path.dirname(file_path).rsplit(os.sep, 2)[-2:]
        if len(dz_info) != 2:
            raise Exception("文件存放路径异常! 必须放在[plate%sauthor]之下!" % os.sep)

        suffix = os.path.splitext(file_path)[-1]
        suffix = suffix if suffix else ""
        return dz_info[0], dz_info[1], suffix

    @staticmethod
    def get_plate_map_conf(plate_map_string):
        """转换从数据库导出的数据.

            SELECT fid, name FROM `bbs_forum_forum` WHERE status=1 AND type= 'forum';
            :parameter plate_map_string:
        """

        dict_data = {}
        lines = plate_map_string.split("\n")
        for line in lines:
            key_value_list = line.strip(" ").strip("|").split("|")
            if len(key_value_list) < 2:
                continue
            dict_key = pinyin.get_pinyin(key_value_list[1]).lower()
            dict_data[dict_key] = int(key_value_list[0])

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
        """移动.

            :parameter new_path
        """

        if not os.path.exists(self.path):
            raise IOError("Path Not Exist!")

        if not os.path.exists(new_path):
            os.makedirs(new_path)

        shutil.move(self.path, new_path)

    def copy(self, new_path):
        """移动.

            :parameter new_path
        """

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
        """批量移动文件列表.

            :parameter entities_list
        """

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
