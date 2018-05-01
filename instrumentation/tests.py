from django.core.management import call_command
from django.test import TestCase


# Create your tests here.
class CommandsTestCase(TestCase):

    def test_schema_export(self):
        """

        :return:
        """

        args = [
            'export_test.yml'
        ]
        opts = {}
        call_command('schema_export', *args, **opts)

    def test_schema_import(self):
        """

        :return:
        """

        args = [
            'import_test.yml'
        ]
        opts = {}
        call_command('schema_import', *args, **opts)
