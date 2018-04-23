import logging

import os
import visa
from django.conf import settings

from instrumentation.models import EquipmentModel

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'muadib.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'DevelopmentConfiguration')

import configurations


configurations.setup()


logger = logging.getLogger(__name__)


class Driver(object):
    def __init__(self, resource):
        self._resource = resource

    @property
    def resource(self):
        return self._resource

    def close(self):
        raise NotImplementedError('')


class DriverManager(object):

    def __init__(self):
        self._resource_manager = self.resource_manager_factory()

    def resources(self):
        return list(self._resource_manager.list_resources())

    def resource_factory(self):
        raise NotImplementedError('')

    def resource_manager_factory(self):
        raise NotImplementedError('')

    def attach(self, equipment_entity: EquipmentModel):
        raise NotImplementedError('')

    def detach(self, driver: Driver):
        driver.close()

class VisaDriver(Driver):

    def __init__(self, resource: visa.Resource):
        super().__init__(resource)

    def close(self):
        self._resource.close()

    def query(self, *args):
        self._resource.query(''.join(args))

    def read(self):
        return self._resource.read()

    def write(self, *args):
        self._resource.write(''.join(args))


class VisaDriverManager(DriverManager):

    def resource_manager_factory(self):
        return visa.ResourceManager(visa_library=settings.VISA_LIBRARY)

    def resource_factory(self, address):
        self._resource_manager.open_resource(resource_name=address)


class DeviceManager(object):

    QUEUES = {}

    def setup(self):
        # Attach all equipment
        for equipment in EquipmentModel.objects.all():
            self.QUEUES[equipment.distinguished_name] = equipment.attache_queue()
            logger.info('Setup queue for equipment[%s]' % equipment)

    def status(self, dn):
       pass
