# Para ejecutar la app:

### Crear las siguientes variables de entorno:

    $ export APP_SETTINGS_MODULE=config.local
    $ export FLASK_APP=entrypoint
    $ export FLASK_ENV=development

### Ejecutar la aplicación

    $ flask run

### Arrancar celery
    
    celery -A celery_worker.celery -l info

### Arrancar tareas programadas
    
    celery -A celery_worker.celery beat -l info

### Arrancar rabbitmq

    sudo rabbitmq-server
