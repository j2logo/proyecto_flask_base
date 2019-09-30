"""

AUTOR: Juanjo

FECHA DE CREACIÓN: 27/09/2019

"""

import logging

from flask import Blueprint, render_template

from app.weather.exceptions import CustomWeatherException
from app.weather.helpers import average_temperature_of_today
from app.weather.models import TempRecord

logger = logging.getLogger(__name__)

weather_bp = Blueprint('weather_bp', __name__, template_folder='templates')


@weather_bp.route("/", methods=['GET'])
def index():
    records = TempRecord.get_all()
    template_context = dict()
    template_context['records'] = records
    template_context['title'] = 'Listado de temperaturas - Flask PyConES19'
    return render_template("weather/index.html", **template_context)


@weather_bp.route("/temp/today/avg", methods=['GET'])
def average_temp():
    avg = average_temperature_of_today()
    template_context = dict()
    template_context['avg'] = avg
    template_context['title'] = 'Temperatura media de hoy - Flask PyConES19'
    return render_template("weather/average.html", **template_context)


@weather_bp.route('/error/<int:num>', methods=['GET'])
def show_error(num):
    if num == 10:
        raise CustomWeatherException('Has introducido el número 10')
    else:
        return index()
