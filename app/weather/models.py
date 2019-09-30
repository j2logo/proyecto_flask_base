"""

AUTOR: Juanjo

FECHA DE CREACIÓN: 27/09/2019

"""

import datetime

from sqlalchemy import and_

from app.db import db, BaseModelMixin


class TempRecord(db.Model, BaseModelMixin):

    id = db.Column(db.Integer, primary_key=True)
    fetched = db.Column(db.DateTime, nullable=False)
    temp = db.Column(db.Float, nullable=False)

    def __init__(self, temp, fetched=None):
        self.temp = temp
        if fetched is None:
            self.fetched = datetime.datetime.utcnow()
        else:
            self.fetched = fetched

    def __str__(self):
        return f'Temp: {self.temp} | Fetched: {self.fetched}'

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def get_records_between_dates(start, end):
        return TempRecord.query.filter(and_(TempRecord.fetched >= start, TempRecord.fetched < end)).all()
