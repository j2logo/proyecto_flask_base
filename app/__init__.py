"""

AUTOR: Juanjo

FECHA DE CREACIÓN: 26/09/2019

"""

import logging
from logging.handlers import SMTPHandler

from flask import Flask, jsonify
from flask_restful import Api

from app.common import http_status
from app.common.error_handling import NoValidParamsError, ObjectNotFound, MultipleObjectsFound, AppErrorBaseClass
from app.db import db
from app.ext import ma, migrate, celery
from app import weather
from app.weather.resources import weather_api_bp
from app.weather.routes import weather_bp

logger = logging.getLogger(__name__)


def create_app(settings_module):
    app = Flask(__name__, instance_relative_config=True)
    # Load the config file specified by the APP environment variable
    app.config.from_object(settings_module)
    # Load the configuration from the instance folder
    if not app.config.get('TESTING', False):
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_pyfile('config-testing.py', silent=True)

    configure_logging(app)

    # Init third party modules
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    init_celery(app)

    # Init custom modules
    weather.init_app(app)

    # Catch al 404 errors
    Api(app, catch_all_404s=True)

    # Disable strict slashes
    app.url_map.strict_slashes = False

    # Blueprints registration
    app.register_blueprint(weather_bp)
    app.register_blueprint(weather_api_bp)

    # Custom error handlers
    register_error_handlers(app)

    return app


def register_error_handlers(app):
    """
    Registers custom error handlers to return JSON responses
    :param app: app instance
    :return: error response as JSON
    """

    @app.errorhandler(Exception)
    def handle_exception_error(e):
        return jsonify({'msg': 'Internal server error'}), http_status.HTTP_500_INTERNAL_SERVER_ERROR

    @app.errorhandler(http_status.HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500_error(e):
        return jsonify({'msg': 'Internal server error'}), http_status.HTTP_500_INTERNAL_SERVER_ERROR

    @app.errorhandler(http_status.HTTP_405_METHOD_NOT_ALLOWED)
    def handle_405_error(e):
        return jsonify({'msg': 'Method not allowed'}), http_status.HTTP_405_METHOD_NOT_ALLOWED

    @app.errorhandler(http_status.HTTP_403_FORBIDDEN)
    def handle_403_error(e):
        return jsonify({'msg': 'Forbidden error'}), http_status.HTTP_403_FORBIDDEN

    @app.errorhandler(http_status.HTTP_404_NOT_FOUND)
    def handle_404_error(e):
        return jsonify({'msg': 'Not Found error'}), http_status.HTTP_404_NOT_FOUND

    @app.errorhandler(AppErrorBaseClass)
    def handle_no_valid_params_error(e):
        return jsonify({'msg': str(e)}), http_status.HTTP_500_INTERNAL_SERVER_ERROR

    @app.errorhandler(NoValidParamsError)
    def handle_no_valid_params_error(e):
        return jsonify({'msg': str(e)}), http_status.HTTP_400_BAD_REQUEST

    @app.errorhandler(ObjectNotFound)
    def handle_object_not_found_error(e):
        return jsonify({'msg': str(e)}), http_status.HTTP_404_NOT_FOUND

    @app.errorhandler(MultipleObjectsFound)
    def handle_no_valid_params_error(e):
        return jsonify({'msg': str(e)}), http_status.HTTP_500_INTERNAL_SERVER_ERROR


def configure_logging(app):
    """
    Configures the logging module. Sets the handlers up for each logger.

    :param app: Flask app instance

    """

    loggers = [app.logger, logging.getLogger('app'), ]
    # Delete default logger handlers
    for l in loggers:
        del l.handlers[:]

    handlers = []

    if (app.config['APP_ENV'] == app.config['APP_ENV_LOCAL']) or (
            app.config['APP_ENV'] == app.config['APP_ENV_TESTING']):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(verbose_formatter())
        handlers.append(console_handler)
    elif app.config['APP_ENV'] == app.config['APP_ENV_DEVELOPMENT']:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(verbose_formatter())
        handlers.append(console_handler)
    elif app.config['APP_ENV'] == app.config['APP_ENV_PRODUCTION']:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(verbose_formatter())
        handlers.append(console_handler)

        mail_handler = SMTPHandler((app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                                   app.config['DONT_REPLY_FROM_EMAIL'],
                                   app.config['ADMINS'],
                                   '[Error][{}] La aplicación falló'.format(app.config['APP_ENV']),
                                   (app.config['MAIL_USERNAME'],
                                    app.config['MAIL_PASSWORD']),
                                   ())

        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(mail_handler_formatter())
        handlers.append(mail_handler)

    for logger in loggers:
        for handler in handlers:
            logger.addHandler(handler)
        logger.propagate = False
        logger.setLevel(logging.DEBUG)


def mail_handler_formatter():
    return logging.Formatter(
        '''
            Message type:       %(levelname)s
            Location:           %(pathname)s:%(lineno)d
            Module:             %(module)s
            Function:           %(funcName)s
            Time:               %(asctime)s.%(msecs)d

            Message:

            %(message)s
        ''',
        datefmt='%d/%b/%Y %H:%M:%S'
    )


def verbose_formatter():
    return logging.Formatter(
        '[%(asctime)s.%(msecs)d]\t %(levelname)s \t[%(name)s.%(funcName)s:%(lineno)d]\t %(message)s',
        datefmt='%d/%b/%Y %H:%M:%S'
    )


def init_celery(app):
    """
    Configures the Celery object (celery) and then creates a subclass of the task that wraps the task execution in
    an application context.

    :param app: Flask app instance

    """

    celery.conf.update(
        broker_url=app.config['BROKER_URL'],
        task_default_queue=app.config['TASK_DEFAULT_QUEUE'],
        task_default_exchange=app.config['TASK_DEFAULT_EXCHANGE'],
        task_default_routing_key=app.config['TASK_DEFAULT_ROUTING_KEY'],
        beat_schedule=app.config['BEAT_SCHEDULE'],
        imports=app.config['TASK_IMPORTS'],
    )
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
