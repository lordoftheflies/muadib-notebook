from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase

# Create your tests here.
from django.utils import timezone
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from instrumentation.models import ConsoleCommandModel
from instrumentation.tasks import terminal_input


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


class InstrumentationTaskTestCase(TestCase):

    @patch('instrumentation.tasks.terminal_input')  # < patching Product in module above
    def test_success(self, product_order):
        product = ConsoleCommandModel.objects.create(
            request='noop',
        )

        terminal_input("kacsa")
        #
        # send_order(product.pk, 3, Decimal(30.3))
        # product_order.assert_called_with(3, Decimal(30.3))

    # @patch('proj.tasks.Product.order')
    # @patch('proj.tasks.send_order.retry')
    # def test_failure(self, send_order_retry, product_order):
    #     product = Product.objects.create(
    #         name='Foo',
    #     )
    #
    #     # Set a side effect on the patched methods
    #     # so that they raise the errors we want.
    #     send_order_retry.side_effect = Retry()
    #     product_order.side_effect = OperationalError()
    #
    #     with raises(Retry):
    #         send_order(product.pk, 3, Decimal(30.6))


class TerminalApiTests(APITestCase):

    def test_readline(self):
        """
        Ensure we can create a new account object.
        """
        url = '/instrumentation/api/terminal/'
        data = {
            'request_timestamp': timezone.now(),
            'request': 'DabApps',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ConsoleCommandModel.objects.count(), 1)
        self.assertEqual(ConsoleCommandModel.objects.get().request, 'DabApps')
