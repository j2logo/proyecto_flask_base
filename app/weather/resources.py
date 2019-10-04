"""

AUTOR: Juanjo

FECHA DE CREACIÓN: 27/09/2019

"""

import logging

from flask import Blueprint, jsonify, current_app
from flask_restful import Api, Resource

from app.weather.exceptions import CustomWeatherException, NoTempsForTodayException
from app.weather.helpers import average_temperature_of_today
from app.weather.models import TempRecord
from app.weather.schemas import TempRecordSchema

logger = logging.getLogger(__name__)

weather_api_bp = Blueprint('temp_api_bp', __name__)

api = Api(weather_api_bp)
temp_record_schema = TempRecordSchema()


class TempListResource(Resource):
    def get(self):
        logger.info('Obteniendo el listado de temperaturas')
        current_app.logger.info('Obteniendo el listado de temperaturas')
        records = TempRecord.get_all()
        response = temp_record_schema.dump(records, many=True)
        return response


class AvgTempResource(Resource):
    def get(self):
        try:
            avg = average_temperature_of_today()
            return jsonify({'avg': avg})
        except NoTempsForTodayException:
            return jsonify({'error': 'No hay temperaturas'})


class ErrorResource(Resource):
    def get(self, num):
        if num == 10:
            raise CustomWeatherException('Has introducido el número 10')
        else:
            return jsonify({'Hello': 'World :)'})


api.add_resource(TempListResource, '/api/temp', endpoint='temp_list_resource')
api.add_resource(AvgTempResource, '/api/temp/today/avg', endpoint='avgtemp_resource')
api.add_resource(ErrorResource, '/api/error/<int:num>', endpoint='error_resource')
