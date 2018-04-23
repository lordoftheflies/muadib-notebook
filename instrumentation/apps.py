import logging

from django.apps import AppConfig
from kombu import Queue

from instrumentation.drivers import dm


class InstrumentationConfig(AppConfig):
    name = 'instrumentation'

    def ready(self):
        super().ready()

        dm.run()

