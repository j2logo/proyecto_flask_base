"""

AUTOR: Juanjo

FECHA DE CREACIÓN: 27/09/2019

"""

from marshmallow import fields

from app.ext import ma


class TempRecordSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    fetched = fields.DateTime()
    temp = fields.Float()
