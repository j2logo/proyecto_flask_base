"""

AUTOR: Juanjo

FECHA DE CREACIÓN: 27/09/2019

"""
from app.weather.exceptions import WeatherException
from app.weather.error_callbacks import weather_error_callback, custom_error_callback
from app.weather.exceptions import WeatherException, CustomWeatherException


def init_app(app):
    _set_error_handlers_callbacks(app)


def _set_error_handlers_callbacks(app):

    @app.errorhandler(WeatherException)
    def handle_weather_exception(e):
        return weather_error_callback(str(e))

    @app.errorhandler(CustomWeatherException)
    def handle_custom_weather_exception(e):
        return custom_error_callback(str(e))
