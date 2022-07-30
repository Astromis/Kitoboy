import datetime

from sqlalchemy.exc import IntegrityError, InterfaceError
from sqlalchemy import desc
from app.app import db
from app.errors.error_handler import DbException


class AbsModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    @property
    def fields(self):
        return self.__table__.columns

    @classmethod
    def create(cls, **kwargs):
        obj = cls(**kwargs)
        try:
            db.session.add(obj)
            db.session.commit()
            return obj
        except (IntegrityError, InterfaceError):
            db.session.rollback()
            raise DbException(f'There was an error in {cls} '
                              f'with params {kwargs} while creating record')
        except Exception as exp:
            db.session.rollback()
            raise exp.__class__

    def update(self, **kwargs):
        for field, value in kwargs.items():
            if field in set(self.fields.keys()):
                self.__setattr__(field, value)
        try:
            db.session.commit()
        except (IntegrityError, InterfaceError):
            db.session.rollback()
            raise DbException(f'There was an error in {self} '
                              f'with params {kwargs} while updating record')
        except Exception as exp:
            db.session.rollback()
            raise exp.__class__

    @classmethod
    def drop_all(cls):
        try:
            db.session.query(cls).delete()
            db.session.commit()

        except (IntegrityError, InterfaceError):
            db.session.rollback()
            raise DbException(f'There was an error in {cls} '
                              f'while deleting all records')
        except Exception as exp:
            db.session.rollback()
            raise exp.__class__

    def delete_item(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except (IntegrityError, InterfaceError):
            db.session.rollback()
            raise DbException(f'There was an error in {self} '
                              f'while deleting record')
        except Exception as exp:
            db.session.rollback()
            raise exp.__class__

    @classmethod
    def get_list(cls, sort=None, **kwrags):
        if sort:
            return list(
                cls.query.filter_by(**kwrags).order_by(desc(cls.created_at)))
        query_list = list(cls.query.filter_by(**kwrags))
        return query_list

    @classmethod
    def get(cls, **kwrags):
        query_result = cls.query.filter_by(**kwrags).first()
        return query_result

    @classmethod
    def get_limit(cls, amount):
        return cls.query.limit(amount).all()

    @classmethod
    def get_all(cls):
        query_result = cls.query.all()
        return query_result

    def get_dict(self):
        result_dict = dict()
        for field in self.fields.keys():
            result_dict[field] = self.__getattribute__(field)
            if isinstance(result_dict[field], datetime.datetime):
                result_dict[field] = str(result_dict[field])
        return result_dict

