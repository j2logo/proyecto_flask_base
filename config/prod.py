"""

AUTOR: Juanjo

FECHA DE CREACIÓN: 26/09/2019

"""

from .default import *


SECRET_KEY = '73dc591a8d8a1e2c9b114da68b79cd4f1a75033126761e1832d67ebdc6d5213e2cab0e819f44bd856710456f9396ef8665c0'

APP_ENV = APP_ENV_PRODUCTION

SQLALCHEMY_DATABASE_URI = 'postgresql://user:pass@postgresql_host:5432/flask_pycones19'
