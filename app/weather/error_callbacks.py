"""

AUTOR: Juanjo

FECHA DE CREACIÓN: 27/09/2019

"""

from flask import jsonify, render_template, request

from app.common import http_status


def weather_error_callback(error_string):
    if request.path.startswith('/api'):
        return jsonify({'msg': error_string}), http_status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        return render_template('error_500.html')


def custom_error_callback(error_string):
    if request.path.startswith('/api'):
        return jsonify({'msg': error_string}), http_status.HTTP_400_BAD_REQUEST
    else:
        return render_template('error_400.html')
