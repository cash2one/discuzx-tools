#!usr/bin/env python
# coding: utf-8

import os.path
import string


class Pinyin(object):
    """translate chinese hanzi to pinyin by python, inspired by flyerhzm’s
    `chinese\_pinyin`_ gem

    usage
    -----
    ::
        In [1]: from xpinyin import Pinyin
        In [2]: p = Pinyin()
        In [3]: p.get_pinyin(u"上海")
        Out[3]: 'shanghai'
        In [4]: p.get_initials(u"上")
        Out[4]: 'S'
    请输入utf8编码汉字
    .. _chinese\_pinyin: https://github.com/flyerhzm/chinese_pinyin
    """

    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'Mandarin.dat')

    def __init__(self):
        self.dict = {}
        for line in open(self.data_path):
            k, v = line.split('\t')
            self.dict[k] = v

    def get_pinyin(self, chars=u'你好', splitter=''):
        result = []
        for char in chars:
            if char in string.ascii_letters or char in string.digits:
                result.append(char.lower())
                continue
            key = "%X" % ord(char)
            try:
                result.append(self.dict[key].split(" ")[0].strip()[:-1]
                              .upper())
            except:
                continue
        return splitter.join(result)

    def get_initials(self, chars=u'你好', splitter=' '):
        result = []
        for chs in chars.split(splitter):
            sign = True
            for char in chs:
                if char in string.ascii_letters:
                    if sign:
                        result.append(char.upper())
                        sign = False
                elif char in string.digits:
                    result.append(char)
                    sign = True
                else:
                    sign = True
                    key = "%X" % ord(char)
                    try:
                        result.append(self.dict[key].split(" ")[0][0].upper())
                    except:
                        continue
        return ''.join(result)
