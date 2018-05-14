import json

from django.core.management.commands.runserver import Command as RunCommand
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder

from instrumentation.models import SchemaModel, EquipmentModel


class Command(RunCommand):
    help = 'Display configuration of an equipment'

    def add_arguments(self, parser):
        parser.add_argument('dn', nargs='?', type=str)

    def handle(self, *args, **options):
        equipment_entity = EquipmentModel.objects.get(distinguished_name=options['dn'])
        json_output = serialize('json', [equipment_entity], cls=DjangoJSONEncoder, sort_keys=True, indent=4, ensure_ascii=False)

        self.stdout.write(self.style.SUCCESS('-------------------------------------------------------'))
        self.stdout.write(self.style.SUCCESS('CONFIGURATION of %s' % options['dn']))
        self.stdout.write(self.style.SUCCESS('-------------------------------------------------------'))
        self.stdout.write(json_output)