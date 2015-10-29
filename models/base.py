#!usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals, print_function

from conf.data_config import Base
from conf.logger_config import model_record_log


class BasicBase(Base):
    """抽象基类, 用于封装常用工具.
    """

    __abstract__ = True

    def __to_dict__(self):
        """类实例对象转为dict.
        """
        ret = {}
        for name in dir(self):
            if not name.startswith('_'):
                ret[name] = getattr(self, name)
        return ret

    @staticmethod
    def batch_save(db_session, entities_list):
        """批量保存.
        """

        result = False
        try:
            db_session.add_all(entities_list)
            db_session.commit()
        except Exception, ex:
            model_record_log.exception(ex)
            db_session.rollback()
        else:
            model_record_log.info("OK")
            result = True
        finally:
            db_session.close()
            return result
