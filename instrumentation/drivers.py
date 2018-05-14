import logging

import os
import visa
from django.conf import settings
from kombu import Queue

# from instrumentation.models import EquipmentModel
# from presentation.views import sio

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'muadib.settings')
# os.environ.setdefault('DJANGO_CONFIGURATION', 'DevelopmentConfiguration')
# import configurations
# configurations.setup()

logger = logging.getLogger(__name__)


class Driver(object):
    def __init__(self, resource):
        self._resource = resource

    @property
    def resource(self):
        return self._resource

    def close(self):
        raise NotImplementedError('')

    def query(self, *args) -> str:
        raise NotImplementedError('')

    def read(self) -> str:
        raise NotImplementedError('')

    def write(self, *args) -> None:
        raise NotImplementedError('')


class DriverManager(object):

    def __init__(self):
        self._resource_manager = self.resource_manager_factory()

    def resources(self):
        return list(self._resource_manager.list_resources())

    @property
    def resource_manager(self):
        return self._resource_manager

    def resource_factory(self, address):
        raise NotImplementedError('')

    def driver_factory(self, resource):
        raise NotImplementedError('')

    def resolve_address(self, equipment_entity) -> str:
        raise NotImplementedError('')

    def resource_manager_factory(self):
        raise NotImplementedError('')

    def attach(self, equipment_entity):
        return self.driver_factory(
            resource=self.resource_factory(address=self.resolve_address(equipment_entity=equipment_entity)))

    def detach(self, driver: Driver):
        driver.close()


class VisaDriver(Driver):

    def __init__(self, resource: visa.Resource):
        super().__init__(resource)

    def close(self):
        self._resource.close()

    def query(self, *args) -> str:
        self._resource.query(''.join(args))

    def read(self) -> str:
        return self._resource.read()

    def write(self, *args) -> None:
        self._resource.write(''.join(args))


class VisaDriverManager(DriverManager):

    def resource_manager_factory(self):
        return visa.ResourceManager(visa_library=settings.VISA_LIBRARY)

    def resource_factory(self, address):
        return self._resource_manager.open_resource(resource_name=address)

    def resolve_address(self, equipment_entity) -> str:
        return equipment_entity.address

    def driver_factory(self, resource):
        return VisaDriver(resource=resource)


class Device(object):

    def __init__(self, driver: Driver, equipment, queue: Queue):
        self._driver = driver
        self._equipment = equipment
        self._queue = queue

    @property
    def resource(self):
        return self._driver.resource

    def initialize(self):
        # from presentation.views import sio
        # sio.emit('state', dict(
        #     state='initialized',
        #
        # ))
        pass

    def read(self, **kwargs):
        response_context = dict()
        for key in kwargs.keys():
            response_context[key] = str(self._driver.read())
        return response_context

    def write(self, **kwargs):
        for key in kwargs.keys():
            kwargs[key] = self._driver.write(str(kwargs[key]))

    def query(self, **kwargs):
        response_context = dict()
        for key in kwargs.keys():
            response_context[key] = self._driver.query(str(kwargs[key]))
        return response_context



class DeviceManager():
    QUEUES = {}
    DRIVER_MANAGER = VisaDriverManager()

    def __init__(self) -> None:
        super().__init__()
        self._devices = dict()


    @property
    def resource_manager(self):
        return self.DRIVER_MANAGER.resource_manager

    def run(self):
        # Attach all equipment
        from instrumentation.models import EquipmentModel
        for equipment_entity in EquipmentModel.objects.all():
            logger.warning('Initialize equipment[%s] ...' % equipment_entity.distinguished_name)
            queue = equipment_entity.attache_queue()
            logger.info('Queue for equipment[%s] opened successfully' % equipment_entity)
            driver = self.DRIVER_MANAGER.attach(equipment_entity=equipment_entity)
            logger.info('Resource for equipment[%s] attached successfully' % equipment_entity)
            device = Device(
                driver=driver,
                queue=queue,
                equipment=equipment_entity
            )
            self._devices[equipment_entity.distinguished_name] = device

    def device(self, dn) -> Device:
        return self._devices[dn]


dm = DeviceManager()
