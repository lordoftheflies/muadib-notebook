from __future__ import absolute_import, unicode_literals

import os

import eventlet
from celery import Celery

# set the default Django settings module for the 'celery' program.
from celery.signals import celeryd_init


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'muadib.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'DevelopmentConfiguration')

import configurations


configurations.setup()

from instrumentation.drivers import dm


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

@celeryd_init.connect
def configure_workers(sender=None, conf=None, **kwargs):
    # if sender in ('worker1@example.com', 'worker2@example.com'):
    #     conf.task_default_rate_limit = '10/m'
    # if sender == 'worker3@example.com':
    #     conf.worker_prefetch_multiplier = 0
    dm.run()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
