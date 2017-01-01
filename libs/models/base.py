#!usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals, print_function

from autoloads import Entity, EntityHelper

from conf.data_config import Base
from conf.logger_config import model_record_log


class BaseModel(Entity, EntityHelper):
    def __init__(self, **kargs):
        Entity.__init__(self, **kargs)


class BasicBase(Base):
    """抽象基类, 用于封装常用工具.
    """

    __abstract__ = True

    def __to_dict__(self):
        """类实例对象转为dict.
        """
        ret = {}
        for name in dir(self):
            if not name.startswith('_') and name.lower() != "metadata":
                ret[name] = getattr(self, name)
        return ret

    def __save(self, db_session, refresh=True):
        """自保存, 暂不可用.

            :parameter db_session
            :parameter refresh
        """

        try:
            db_session.add(self)
            if refresh:
                db_session.flush()
                db_session.refresh(self)
            db_session.commit()
        except Exception, ex:
            model_record_log.exception(ex)
            db_session.rollback()
        finally:
            db_session.close()

    @staticmethod
    def __batch_save(db_session, entities_list):
        """批量保存, 暂不可用.

            :parameter db_session
            :parameter entities_list
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
