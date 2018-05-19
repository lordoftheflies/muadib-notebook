import uuid
from uuid import UUID

import yaml
from django.core.management.commands.runserver import Command as RunCommand

from instrumentation import models as instrumentation_models


class Command(RunCommand):
    help = 'Import equipment schema'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str)

    def handle(self, *args, **options):

        # data = dict(
        #     spec='1.1',
        #     devices=self.map_schema_to_devices(SchemaModel.objects.all()),
        #     resources=self.map_equipments_to_resources(equipments=EquipmentModel.objects.all())
        # )

        file_path = options['file']
        with open(file_path, mode='r', encoding='utf-8') as stream:
            data = yaml.load(stream=stream)

        if 'devices' in data:
            self.create_devices(data['devices'])

            if 'resources' in data:
                self.create_resources(data['resources'])

        self.stdout.write(self.style.SUCCESS('Schema imported from %s.' % file_path))

    def create_devices(self, devices):
        for device_key in devices.keys():

            device = devices[device_key]

            equipment_kwargs = {}
            equipment_kwargs['name'] = device_key

            if 'name' in device:
                equipment_kwargs['name'] = device['name']
            if 'display_name' in device:
                equipment_kwargs['display_name'] = device_key

            if 'description' in device:
                equipment_kwargs['description'] = device['description']

            schema = instrumentation_models.Equipment.objects.create(**equipment_kwargs)
            if 'properties' in device:
                self.create_properties(device['properties'], schema)
            # if 'dialogues' in device:
            #     self.create_dialogues(device['dialogues'], schema)

    def create_resources(self, resources):
        for resource_key in resources.keys():
            equipment = self.create_resource(resource_key, resources[resource_key])

    def create_resource(self, resource_key, resource):
        return instrumentation_models.Equipment.objects.get(name=resource['device'])

    def create_properties(self, properties, schema: instrumentation_models.Equipment):
        for property_key in properties:
            attribute = self.create_property(property_key, properties[property_key], schema)

    def create_property(self, property_key, property, schema: instrumentation_models.Equipment):
        attribute = instrumentation_models.EquipmentProperty.objects.create(
            name=property_key,
            display_name=property['display_name'] if 'display_name' in property else None,
            description=property['description'] if 'description' in property else None,
            equipment=schema
        )
        return attribute
