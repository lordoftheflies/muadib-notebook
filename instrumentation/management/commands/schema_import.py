import uuid
from uuid import UUID

import yaml
from django.core.management.commands.runserver import Command as RunCommand

from instrumentation.models import SchemaModel, EquipmentModel, SchemaAttributeModel, SchemaActionModel, OperationModel


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
            equipment_kwargs['distinguished_name'] = device_key

            if 'name' in device:
                equipment_kwargs['display_name'] = device['name']
            else:
                equipment_kwargs['display_name'] = device_key

            if 'description' in device:
                equipment_kwargs['description'] = device['description']

            schema = SchemaModel.objects.create(**equipment_kwargs)
            if 'properties' in device:
                self.create_properties(device['properties'], schema)
            if 'dialogues' in device:
                self.create_dialogues(device['dialogues'], schema)

    def create_resources(self, resources):
        for resource_key in resources.keys():
            equipment = self.create_resource(resource_key, resources[resource_key])

    def create_resource(self, resource_key, resource):
        schema = SchemaModel.objects.get(distinguished_name=resource['device'])
        equipment = None
        try:
            equipment = EquipmentModel.objects.get(distinguished_name=schema.distinguished_name)
        except BaseException as e:
            equipment = EquipmentModel.objects.create(
                distinguished_name=schema.distinguished_name,
                display_name=schema.display_name,
                description=schema.description,
                schema=schema,
                address=resource_key
            )
        finally:
            return equipment

    def create_properties(self, properties, schema: SchemaModel):
        for property_key in properties:
            attribute = self.create_property(property_key, properties[property_key], schema)

    def create_property(self, property_key, property, schema: SchemaModel):
        attribute = SchemaAttributeModel.objects.create(
            distinguished_name=property_key,
            display_name=property['name'] if 'name' in property else property_key,
            description=property['description'] if 'description' in property else None,
            read_operation = self.create_operation(property['getter']) if 'getter' in property else None,
            write_operation = self.create_operation(property['setter']) if 'setter' in property else None,
            schema=schema
        )
        return attribute

    def create_dialogues(self, dialogues, schema: SchemaModel):
        for d in dialogues:
            action = self.create_dialogue(d, schema)

    def create_dialogue(self, d, schema: SchemaModel):
        id = uuid.uuid4()
        action = SchemaActionModel.objects.create(
            distinguished_name=d['dn'] if 'dn' in d else id,
            display_name=d['name'] if 'name' in d else id,
            description=d['description'] if 'description' in d else None,
            schema=schema,
            operation = self.create_operation(d)
        )
        return action

    def create_operation(self, op):
        operation =OperationModel.objects.create(
            source=op['q']
        )
        return operation


    def map_resource(self, schema_entity: SchemaModel):
        return dict(
            device=schema_entity.distinguished_name
        )

    def map_schema_to_devices(self, schemas):
        device_map = {}
        for schema in schemas:
            device_map[schema.distinguished_name] = self.map_device(schema)
        return device_map

    def map_equipments_to_resources(self, equipments):
        resource_map = {}
        for e in equipments:
            resource_map[e.address] = self.map_resource(e.schema)
        return resource_map

    def map_device(self, schema_entity: SchemaModel):
        property_map = {a.distinguished_name: self.map_property(a) for a in schema_entity.attributes}
        dialogue_list = [self.map_dialogue(a) for a in schema_entity.actions]
        return dict(
            dn=schema_entity.distinguished_name,
            name=schema_entity.display_name,
            description=schema_entity.description,
            eom=self.map_eom(),
            properties=property_map if property_map.keys() else None,
            dialogues=dialogue_list if dialogue_list else None
        )

    def map_eom(self):
        return {
            'ASRL INSTR': dict(
                q='\\r\\n',
                r='\\n'
            ),
            'USB INSTR': dict(
                q='\\n',
                r='\\n'
            ),
            'TCPIP INSTR': dict(
                q=r'\\n',
                r=r'\\n'
            ),
            'TCPIP SOCKET': dict(
                q=r'\\n',
                r=r'\\n'
            ),
            'GPIB INSTR': dict(
                q=r'\\n',
                r=r'\\n'
            ),
        }

    def map_property(self, attribute_model: SchemaAttributeModel):
        return dict(
            default=attribute_model.data_default,
            getter=self.map_command(attribute_model.read_operation),
            setter=self.map_command(attribute_model.write_operation),
            specs=dict(type=attribute_model.data_type)
        )

    def map_dialogue(self, action_model: SchemaActionModel):
        return self.map_command(action_model.operation)

    def map_command(self, op: OperationModel):
        if op is not None:
            return dict(q=op.source, r='')
        else:
            return None
