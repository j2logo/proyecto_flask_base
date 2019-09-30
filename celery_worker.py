"""

AUTOR: Juanjo

FECHA DE CREACIÓN: 26/09/2019

"""

import os

from app import create_app
from app.ext import celery

app = create_app(os.getenv('APP_SETTINGS_MODULE'))
