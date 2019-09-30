"""

AUTOR: Juanjo

FECHA DE CREACIÓN: 26/09/2019

"""

import os

from flask import jsonify

from app import create_app

settings_module = os.getenv('APP_SETTINGS_MODULE')
app = create_app(settings_module)


@app.route('/test')
def hello():
    return jsonify({"¿Estás ejecutándote?": "¡¡¡Sí!!! La vida es como una caja de bombones, nunca sabes lo que te va a tocar."})
