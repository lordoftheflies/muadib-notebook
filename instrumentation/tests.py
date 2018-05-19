from unittest.mock import patch

from datetime import datetime
from django.test import TestCase
from django.utils import timezone

from instrumentation import models as instrumentation_models



# Create your tests here.

class EquipmentTestCase(TestCase):
    def setUp(self):
        instrumentation_models.Equipment.objects.create(
            name="test_simple_eq",
            description="Simple test equipment"
        )
        instrumentation_models.Equipment.objects.create(
            name="test_single_eq",
            display_name="Simple test equipment with friendly name",
            description="Simple test equipment with friendly name desc"
        )

    def test_friendly_name(self):
        """Test friendly names"""
        test_simple = instrumentation_models.Equipment.objects.get(name="test_simple_eq")
        test_single = instrumentation_models.Equipment.objects.get(name="test_single_eq")
        self.assertEqual(test_simple.friendly_name, 'test_simple_eq')
        self.assertEqual(test_single.friendly_name, 'Simple test equipment with friendly name')

class ProcessTestCase(TestCase):
    def setUp(self):
        instrumentation_models.Process.objects.create(
            name="test_simple",
            description="Simple test process without parameters"
        )
        instrumentation_models.Process.objects.create(
            name="test_single_equipment",
            display_name="Measure with single equipment",
            description="Simple test process without parameters with single equipment"
        )

    def test_friendly_name(self):
        """Test friendly names"""
        test_simple = instrumentation_models.Process.objects.get(name="test_simple")
        test_single_equipment = instrumentation_models.Process.objects.get(name="test_single_equipment")
        self.assertEqual(test_simple.friendly_name, 'test_simple')
        self.assertEqual(test_single_equipment.friendly_name, 'Measure with single equipment')

class ExecuteProcessTestCase(TestCase):
    def setUp(self):
        instrumentation_models.Equipment.objects.create(
            name="test_simple_eq",
            description="Simple test equipment"
        )
        instrumentation_models.Process.objects.create(
            name="test_simple_proc",
            description="Simple test process without parameters"
        )



    def test_execute(self):
        """Test execute process"""
        test_simple_proc = instrumentation_models.Process.objects.get(name="test_simple_proc")

        test_simple_proc.begin().end()

        test_simple_exec = instrumentation_models.Execution.objects.get(id=1)

        self.assertEqual(test_simple_exec.state, instrumentation_models.EXECUTION_STATE_FINISHED)

    def test_execute_wit_data(self):
        """Test execute with data"""
        test_simple_proc = instrumentation_models.Process.objects.get(name="test_simple_proc")

        test_simple_proc.begin().ingest_data(
            param_one='test_text',
            param_two=10.0,
            param_three=11,
            param_four=datetime.strftime(timezone.now(), '%y-%m-%d %H:%M:%S.%f'),
        ).end()

        test_dataframe_0 = instrumentation_models.DataFrame.objects.get(id=1)
        self.assertEqual(test_dataframe_0.raw_data['param_one'], 'test_text')

    def test_execute_wit_data_and_additional(self):
        """Test execute with data and additional"""
        test_simple_proc = instrumentation_models.Process.objects.get(name="test_simple_proc")

        test_simple_proc.begin().ingest_data(
            data_param_str='test_text',
            data_param_float=10.0,
            data_param_int=11,
            data_param_ts=datetime.strftime(timezone.now(), '%y-%m-%d %H:%M:%S.%f'),
        ).ingest_additional(
            additional_param_str='test_text2',
            additional_param_float=12.0,
            additional_param_int=13,
            additional_param_ts=datetime.strftime(timezone.now(), '%y-%m-%d %H:%M:%S.%f'),
        ).end()

        test_dataframe_0 = instrumentation_models.DataFrame.objects.get(id=1)
        self.assertEqual(test_dataframe_0.additional['additional_param_int'], 13)

    def test_execute_wit_data_and_markers(self):
        """Test execute with data and markers"""
        test_simple_proc = instrumentation_models.Process.objects.get(name="test_simple_proc")

        test_simple_proc.begin().ingest_data(
            data_param_str='test_text',
            data_param_float=10.0,
            data_param_int=11,
            data_param_ts=datetime.strftime(timezone.now(), '%y-%m-%d %H:%M:%S.%f'),
        ).ingest_additional(
            marker_param_str='test_text2',
            marker_param_float=12.0,
            marker_param_int=13,
            marker_param_ts=datetime.strftime(timezone.now(), '%y-%m-%d %H:%M:%S.%f'),
        ).end()

    def test_execute_wit_data_and_indicators(self):
        """Test execute with data and indicators"""
        test_simple_proc = instrumentation_models.Process.objects.get(name="test_simple_proc")

        test_simple_proc.begin().ingest_data(
            data_param_str='test_text',
            data_param_float=10.0,
            data_param_int=11,
            data_param_ts=datetime.strftime(timezone.now(), '%y-%m-%d %H:%M:%S.%f'),
        ).ingest_additional(
            indicator_param_str='test_text2',
            indicator_param_float=12.0,
            indicator_param_int=13,
            indicator_param_ts=datetime.strftime(timezone.now(), '%y-%m-%d %H:%M:%S.%f'),
        ).end()

#
# class CommandsTestCase(TestCase):
#
#     def test_schema_export(self):
#         """
#
#         :return:
#         """
#
#         args = [
#             'export_test.yml'
#         ]
#         opts = {}
#         call_command('schema_export', *args, **opts)
#
#     def test_schema_import(self):
#         """
#
#         :return:
#         """
#
#         args = [
#             'import_test.yml'
#         ]
#         opts = {}
#         call_command('schema_import', *args, **opts)
#
#
# class PingEquipment(TestCase):
#
#     @patch('instrumentation.tasks.ping_task')  # < patching Product in module above
#     def test_success(self, a):
#         terminal_task("kacsa", 'kaka')


# class InstrumentationTaskTestCase(TestCase):
#
#     @patch('instrumentation.tasks.terminal_input')  # < patching Product in module above
#     def test_success(self, product_order):
#         product = ConsoleCommandModel.objects.create(
#             request='noop',
#         )
#
#         terminal_input("kacsa", 'kaka')
#         #
#         # send_order(product.pk, 3, Decimal(30.3))
#         # product_order.assert_called_with(3, Decimal(30.3))
#
#     # @patch('proj.tasks.Product.order')
#     # @patch('proj.tasks.send_order.retry')
#     # def test_failure(self, send_order_retry, product_order):
#     #     product = Product.objects.create(
#     #         name='Foo',
#     #     )
#     #
#     #     # Set a side effect on the patched methods
#     #     # so that they raise the errors we want.
#     #     send_order_retry.side_effect = Retry()
#     #     product_order.side_effect = OperationalError()
#     #
#     #     with raises(Retry):
#     #         send_order(product.pk, 3, Decimal(30.6))
#
#
# # class TerminalApiTests(APITestCase):
# #
# #     def test_readline(self):
# #         """
# #         Ensure we can create a new account object.
# #         """
# #         url = '/instrumentation/api/terminal/'
# #         data = {
# #             'request_timestamp': timezone.now(),
# #             'request': 'DabApps',
# #         }
# #         response = self.client.post(url, data, format='json')
# #         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
# #         self.assertEqual(ConsoleCommandModel.objects.count(), 1)
# #         self.assertEqual(ConsoleCommandModel.objects.get().request, 'DabApps')
#
# @pytest.mark.asyncio
# async def test_terminal_consumer():
#     communicator = WebsocketCommunicator(TerminalConsumer, "/terminal/ek895/")
#
#     given = dict(
#         request='PM ON',
#         response='ok'
#     )
#
#     connected, subprotocol = await communicator.connect()
#     assert connected
#     # Test sending text
#     await communicator.send_json_to(content=given)
#     response = await communicator.receive_json_from()
#     assert response == "hello"
#     # Close
#     await communicator.disconnect()
