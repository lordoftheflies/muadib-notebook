import logging

from django.apps import AppConfig
from django.conf import settings
from kombu import Queue

# from instrumentation.drivers import dm

logger = logging.getLogger(__name__)

class InstrumentationConfig(AppConfig):
    name = 'instrumentation'

    def ready(self):
        logger.info('Instrumentation module is ready')
        logger.debug('VISA backend library: %s' % settings.VISA_LIBRARY)

        # dm.run()
        super().ready()
