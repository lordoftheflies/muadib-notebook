import queue
import time
from ipywidgets import widgets


class FormFieldFactory(object):

    def __init__(self):
        pass

    def create_field_interval(self, **kwargs):
        return widgets.IntSlider(
            **kwargs
        )

    def create_field_choice(self, **kwargs):
        return widgets.Dropdown(
            **kwargs
        )

    def create_field_integer(self, **kwargs):
        return widgets.IntText(
            **kwargs
        )


class Driver(object):

    def __init__(self):
        self._locked = False

    @property
    def locked(self) -> bool:
        return self._locked

    @locked.setter
    def locked(self, value: bool):
        self._locked = value

    def query(self, command: str):
        """
        Need to be override by driver
        :param command:
        :return:
        """
        return

    def read(self, command: str):
        """
        Need to be override by driver
        :param command:
        :return:
        """
        return

    def write(self, command: str):
        """
        Need to be override by driver
        :param command:
        :return:
        """
        return

    def open_resource(self):
        pass

    def close_resource(self):
        pass


class VisaDriver(Driver):
    pass


class ModbusDriver(Driver):
    pass


class ParametricalMixin(object):

    def __init__(self, properties: list, **kwargs) -> None:
        super().__init__()
        self._parameters = {
            **kwargs
        }
        self.properties = properties
        self.reset_defaults()

    @property
    def schema(self):
        return self.properties

    def check_configuration(self) -> bool:
        for p in self.properties:
            if 'required' in p.keys() and p['required']:
                if p['name'] not in self._parameters.keys():
                    return False
        return True

    def reset_defaults(self) -> dict:
        for p in self.properties:
            property_name = p['name']
            if property_name not in self._parameters.keys():
                self._parameters[p['name']] = p['default']
        return self._parameters

    def merge_parameters(self, **kwargs):
        self._parameters = {
            **self._parameters,
            **kwargs
        }
        return self._parameters

    def extend_configuration(self, *args):
        self.properties = self.properties + list(args)
        self.reset_defaults()
        return self.properties

    @property
    def parameters(self) -> dict:
        return self._parameters

    @parameters.setter
    def parameters(self, value):
        self._parameters = value


class Equipment(ParametricalMixin):
    properties = [
        dict(name='interval', type=int, min=0, max=100, unit='s'),
        dict(name='period', type=int, min=0, max=100, unit='s'),
    ]

    parameter_keys = [
        'interval',
        'period'
    ]

    def __init__(self, driver: Driver, properties: list, **kwargs) -> None:
        super().__init__(properties, **kwargs)
        self._driver = driver

    def get_output(self):
        return dict(data=[])


class Task(ParametricalMixin):

    def __init__(self, properties, interval=1, period=1, **kwargs) -> None:
        super().__init__(properties, **kwargs)
        self.interval = interval
        self.period = period

    @property
    def range_start(self) -> int:
        return 0

    @property
    def range_end(self) -> int:
        return int(self.interval / self.period)

    def attach_equipment(self, equipment: Equipment):
        self.extend_configuration(*equipment.schema)
        self.merge_parameters(**equipment.parameters)

    def load_equipment(self, equipment: Equipment):
        equipment.merge_parameters(**self.parameters)

    @property
    def parameters(self) -> dict:
        return self._parameters

    @parameters.setter
    def parameters(self, value):
        self._parameters = value
        self._flush_configuration()

    def _flush_configuration(self):
        pass

    def run(self, **kwargs):
        self.pre_process(**{**self.parameters, **kwargs})

        for x in range(self.range_start, self.range_end):
            start_time = time.time()

            yield self.process_step(**self.get_output())

            end_time = time.time()

            sl = self.parameters['period'] - (end_time - start_time)
            if sl > 0:
                time.sleep(sl)

        self.post_process(**{**self.parameters, **kwargs})

    def pre_process(self, **kwargs):
        return dict(**kwargs)

    def process_step(self, **kwargs):
        return dict(**kwargs)

    def post_process(self, **kwargs):
        return dict(**kwargs)


class Queue(queue.Queue):

    def enqueue(self, task: Task):
        self.put(task)
