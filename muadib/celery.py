from __future__ import absolute_import, unicode_literals

import logging
import os
import traceback

from celery import Celery
# set the default Django settings module for the 'celery' program.
from celery.signals import celeryd_init

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'muadib.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'DevelopmentConfiguration')
import configurations

configurations.setup()

from instrumentation import models as instrumentation_models

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
from celery.utils.log import get_logger

logger = get_logger(__name__)


@celeryd_init.connect
def configure_workers(sender=None, conf=None, **kwargs):
    try:
        logger.info('Celery initialization ...')
        active_equipments_queues = instrumentation_models.Equipment.generate_queues()
        active_process_queues = instrumentation_models.Process.generate_queues()
        app.conf.update(task_queues=active_equipments_queues + active_process_queues)
    except:
        traceback.print_exc()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@app.task(bind=True)
def ping_task(self):
    print('Request: {0!r}'.format(self.request))
    return True
