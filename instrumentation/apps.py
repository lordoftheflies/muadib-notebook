import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class InstrumentationConfig(AppConfig):
    name = 'instrumentation'

    def ready(self):
        super().ready()


class DeviceManager(object):

    def setup(self):
        # Attach all equipment
        from instrumentation.models import EquipmentModel
        [equipment.attache_queue() and logger.info('Setup queue for equipment[%s]' % equipment) for equipment in
         EquipmentModel.objects.all()]
