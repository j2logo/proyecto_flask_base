"""

AUTOR: Juanjo

FECHA DE CREACIÓN: 26/09/2019

"""

from flask_sqlalchemy import SQLAlchemy

from app.common.error_handling import ObjectNotFound

db = SQLAlchemy()


class BaseModelMixin:

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_object_or_404(cls, id):
        o = cls.get_by_id(id)
        if o is not None:
            return o
        else:
            raise ObjectNotFound(f'The object whose id is {id} does not exist')

    @classmethod
    def simple_filter(cls, **kwargs):
        return cls.query.filter_by(**kwargs).all()
