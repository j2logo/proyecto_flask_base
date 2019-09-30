"""

AUTOR: Juanjo

FECHA DE CREACIÓN: 26/09/2019

"""

from celery import Celery
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

ma = Marshmallow()
migrate = Migrate()
celery = Celery('flask_PyConES19')
