import logging

from django.apps import AppConfig
from kombu import Queue



class InstrumentationConfig(AppConfig):
    name = 'instrumentation'

    def ready(self):
        super().ready()

