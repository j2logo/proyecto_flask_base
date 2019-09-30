"""

AUTOR: Juanjo

FECHA DE CREACIÓN: 27/09/2019

"""

import datetime
import random

from app.ext import celery
from app.weather.models import TempRecord


@celery.task()
def fetch_temp():
    """
    Esta función es un fake que simula la captura de temperatura de un sensor
    generando un número aleatorio
    """
    rand_init = random.SystemRandom()
    random_temp = round(rand_init.uniform(0, 45), 1)
    temp_record = TempRecord(random_temp, datetime.datetime.utcnow())
    temp_record.save()
