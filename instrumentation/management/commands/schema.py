import json

from django.core.management.commands.runserver import Command as RunCommand
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder

from instrumentation.models import SchemaModel

class Command(RunCommand):
    help = 'Display scheme of the station controller'

    def add_arguments(self, parser):
        parser.add_argument('dn', nargs='?', type=str)

    def handle(self, *args, **options):
        if 'dn' in options.keys() and options['dn'] is not None:
            schema = SchemaModel.objects.get(distinguished_name=options['dn'])
            json_output = serialize('json', [schema], cls=DjangoJSONEncoder, sort_keys=True, indent=4, ensure_ascii=False)
        else:
            schemas = SchemaModel.objects.all()

            json_output = serialize('json', schemas, cls=DjangoJSONEncoder, sort_keys=True, indent=4, ensure_ascii=False)

        self.stdout.write(self.style.SUCCESS('-------'))
        self.stdout.write(self.style.SUCCESS('SCHEMAS'))
        self.stdout.write(self.style.SUCCESS('-------'))
        self.stdout.write(json_output)