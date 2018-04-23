from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'muadib.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'DevelopmentConfiguration')

import configurations


configurations.setup()

app = Celery('muadib')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.task_default_queue = 'default'

# in the app bootstraping
# eventlet.monkey_patch()
# server = socketio.()
# socketio.init_app(app, message_queue=app.conf.broker_url)


# app.conf.task_routes = {
#     'instrumentation.tasks.status': {
#         'queue': 'feeds'
#     }
# }


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
