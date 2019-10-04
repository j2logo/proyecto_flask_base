"""

AUTOR: Juanjo

FECHA DE CREACIÓN: 27/09/2019

"""

import datetime

from app.weather.exceptions import NoTempsForTodayException
from app.weather.models import TempRecord


def average_temperature_of_today():
    today = datetime.datetime.utcnow().date()
    today_dt = datetime.datetime(today.year, today.month, today.day, 0, 0)
    tomorrow_dt = today_dt + datetime.timedelta(days=1)
    today_records = TempRecord.get_records_between_dates(today_dt, tomorrow_dt)
    if len(today_records) == 0:
        raise NoTempsForTodayException('No se han registrado temperaturas en el día de hoy')
    temp_add = 0
    for r in today_records:
        temp_add += r.temp
    return round(temp_add/len(today_records), 1)
