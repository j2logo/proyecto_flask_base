"""

AUTOR: Juanjo

FECHA DE CREACIÓN: 26/09/2019

"""

from os.path import abspath, dirname

# Define the application directory
BASE_DIR = dirname(dirname(abspath(__file__)))

SECRET_KEY = '871d81215a36d15d11862bbaea6bd1d6b37f00c7fef492d207777cfbf05cde32a07bd6b9feacbd5be5e1e03d46c417673cab'

PROPAGATE_EXCEPTIONS = True

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Database configuration
SQLALCHEMY_DATABASE_URI = ''
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 5,
    'pool_timeout': 10
}
SQLALCHEMY_TRACK_MODIFICATIONS = False
SHOW_SQLALCHEMY_LOG_MESSAGES = False

# Disables suggestions of other endpoints that closely match the requested endpoint (flask-restful)
ERROR_404_HELP = False

# Email settings
MAIL_SERVER = 'mail.yourserver.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_DEBUG = False
MAIL_USERNAME = 'email@address.com'
MAIL_PASSWORD = 'xxx'
MAIL_DEFAULT_SENDER = 'No Reply <no-reply@address.com>'
DONT_REPLY_FROM_EMAIL = MAIL_DEFAULT_SENDER

# App admins
ADMINS = ['juanjo@j2logo.com', ]

# App environments
APP_ENV_LOCAL = 'local'
APP_ENV_DEVELOPMENT = 'development'
APP_ENV_TESTING = 'testing'
APP_ENV_PRODUCTION = 'production'
APP_ENV = ''

# Celery conf

BROKER_URL = 'amqp://guest:guest@localhost:5672//'
TASK_DEFAULT_QUEUE = 'flask_pycones19'
TASK_DEFAULT_EXCHANGE = 'flask_pycones19'
TASK_DEFAULT_ROUTING_KEY = 'flask_pycones19'
TASK_IMPORTS = ['app.weather.tasks', ]

BEAT_SCHEDULE = {
    'remind_general_event':  {
        'task': 'app.weather.tasks.fetch_temp',
        'schedule': 3600
    },
}
