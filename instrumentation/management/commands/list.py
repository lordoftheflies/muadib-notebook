import json

from django.core.management.commands.runserver import Command as RunCommand
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder

from instrumentation.models import SchemaModel, EquipmentModel
from muadib import sio


class Command(RunCommand):
    help = 'Display equipments of the station controller'

    def handle(self, *args, **options):
        schemas = EquipmentModel.objects.all()
        json_output = serialize('json', schemas, cls=DjangoJSONEncoder, sort_keys=True, indent=4, ensure_ascii=False)

        self.stdout.write(self.style.SUCCESS('----------'))
        self.stdout.write(self.style.SUCCESS('EQUIPMENTS'))
        self.stdout.write(self.style.SUCCESS('----------'))
        self.stdout.write(json_output)