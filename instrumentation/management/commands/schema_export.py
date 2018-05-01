import yaml
from django.core.management.commands.runserver import Command as RunCommand

from instrumentation.models import SchemaModel, EquipmentModel, SchemaAttributeModel, SchemaActionModel, OperationModel


class Command(RunCommand):
    help = 'Export equipment schema'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str)

    def handle(self, *args, **options):

        data = dict(
            spec='1.1',
            devices=self.map_schema_to_devices(SchemaModel.objects.all()),
            resources=self.map_equipments_to_resources(equipments=EquipmentModel.objects.all())
        )

        file_path = options['file']
        with open(file_path, mode='wt', encoding='utf-8') as stream:
            yaml.dump(
                data=data,
                stream=stream,
                default_flow_style=False,
                allow_unicode=True,
                encoding='utf-8',
                indent=4,
                line_break=True,
            )

        self.stdout.write(self.style.SUCCESS('Schema exported to %s.' % file_path))

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
