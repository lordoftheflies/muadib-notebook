import unittest

from muadib_utils import Driver, ModbusDriver, VisaDriver, Equipment, Task, Queue


class DriverTestCase(unittest.TestCase):

    def setUp(self):
        self.driver = Driver()
        pass

    def test_open_resource(self):
        self.driver.open_resource()

    def test_close_resource(self):
        self.driver.close_resource()


class VisaDriverTestCase(DriverTestCase):

    def setUp(self):
        self.driver = VisaDriver()
        pass


class ModbusDriverTestCase(DriverTestCase):

    def setUp(self):
        self.driver = ModbusDriver()
        pass


class EquipmentTestCase(unittest.TestCase):

    def setUp(self):
        self.equipment = Equipment(
            driver=Driver(),
            properties=[
                dict(name='start_frequency', default=100, unit='Hz')
            ])
        pass

    def test_parameters(self):
        self.assertEqual(self.equipment.parameters, {
            'start_frequency': 100
        })

    def test_schema_change(self):
        self.equipment.extend_configuration(
            dict(name='stop_frequency', default=200, unit='Hz'),
            dict(name='interval', default=1, unit='s'),
            dict(name='period', default=10, unit='s')
        )
        self.assertEqual(self.equipment.parameters, {
            'start_frequency': 100,
            'stop_frequency': 200,
            'interval': 1,
            'period': 10
        })


class TaskTestCase(unittest.TestCase):

    def setUp(self):
        self.task = Task()
        pass


class QueueTestCase(unittest.TestCase):

    def setUp(self):
        self.queue = Queue()
        pass


if __name__ == '__main__':
    unittest.main()
