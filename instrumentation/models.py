import json
import logging

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
# Create your models here.
from kombu import Queue, Exchange

logger = logging.getLogger(__name__)


class Content(models.Model):
    class Meta:
        abstract = True

    display_name = models.CharField(max_length=100, null=True, blank=True, default=None)
    description = models.CharField(max_length=1000, null=True, blank=True, default=None)


class Entity(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=100)


class NamedEntity(Entity, Content):
    class Meta:
        abstract = True

    @property
    def friendly_name(self):
        return self.display_name if self.display_name is not None else self.name

    def __str__(self):
        return self.friendly_name


DATA_TYPE_TEXT = 'text'
DATA_TYPE_NUMBER = 'number'
DATA_TYPE_DATE = 'date'

DATA_TYPES = [
    (DATA_TYPE_DATE, _('Date')),
    (DATA_TYPE_NUMBER, _('Number')),
    (DATA_TYPE_TEXT, _('Text')),
]

EXECUTION_STATE_PENDING = 'pending'
EXECUTION_STATE_RUNNING = 'running'
EXECUTION_STATE_FAIL = 'failed'
EXECUTION_STATE_FINISHED = 'finished'

EXECUTION_STATES = [
    (EXECUTION_STATE_FAIL, _('Failed')),
    (EXECUTION_STATE_FINISHED, _('Finished')),
    (EXECUTION_STATE_PENDING, _('Pending')),
    (EXECUTION_STATE_RUNNING, _('Running')),
]


class Variable(NamedEntity):
    data_type = models.CharField(max_length=100, choices=DATA_TYPES, default=DATA_TYPE_TEXT)
    value = models.CharField(max_length=100, null=True, blank=True, default=None)


class Parameter(NamedEntity):
    data_type = models.CharField(max_length=100, choices=DATA_TYPES, default=DATA_TYPE_TEXT)
    default_value = models.CharField(max_length=100, null=True, blank=True, default=None)
    required = models.NullBooleanField(default=None, null=True, blank=True)
    minimum = models.FloatField(default=None, null=True, blank=True)
    maximum = models.FloatField(default=None, null=True, blank=True)

    class Meta:
        abstract = True


class Equipment(NamedEntity):
    EXCHANGE_NAME = 'equipment'

    active = models.BooleanField(default=True)

    def create_queue(self, exchange: Exchange):
        queue = Queue(
            name=self.name,
            exchange=exchange,
            routing_key='%s' % self.name)
        logger.info('Create queue %s:%s' % (exchange.name, queue.name))
        return queue

    @staticmethod
    def generate_queues():
        exchange = Exchange(Equipment.EXCHANGE_NAME, 'direct', durable=True)
        return [e.create_queue(exchange=exchange) for e in Equipment.objects.filter(active=True)]

    @property
    def properties(self):
        return EquipmentProperty.objects.filter(equipment=self)


class EquipmentProperty(Parameter):
    equipment = models.ForeignKey(
        verbose_name=_('Equipment'),
        to=Equipment,
        related_name='equipment_properties',
        on_delete=models.CASCADE
    )


class Process(NamedEntity):
    EXCHANGE_NAME = 'process'

    """
    Folyamat entitás.
    """
    equipments = models.ManyToManyField(to=Equipment, related_name='processes')

    @property
    def input_parameters(self):
        return ProcessParameter.objects.filter(process=self)

    def begin(self, **kwargs):
        execution = Execution.objects.create(process=self)
        configuration = {p.name: p.default_value if p.name not in kwargs.keys() else kwargs[p.name] for p in
                         self.input_parameters}
        execution.configuration = configuration
        execution.state = EXECUTION_STATE_PENDING
        execution.save()
        logger.warning('Process[%s] create new execution[%s]' % (self.name, execution.id))
        return execution

    def create_queue(self, exchange: Exchange):
        queue = Queue(
            name=self.name,
            exchange=exchange,
            routing_key='%s' % self.name)
        logger.info('Create queue %s:%s' % (exchange.name, queue.name))

        return queue

    @staticmethod
    def generate_queues():
        exchange = Exchange(Process.EXCHANGE_NAME, 'direct', durable=True)
        return [p.create_queue(exchange=exchange) for p in Process.objects.all()]

    @property
    def executions(self):
        return Execution.objects.filter(process=self)

class ProcessParameter(Parameter):
    process = models.ForeignKey(
        verbose_name=_('Process'),
        to=Process,
        on_delete=models.CASCADE
    )


class Execution(models.Model):
    root_task_id = models.UUIDField(null=True, blank=True, default=None)
    process = models.ForeignKey(
        verbose_name=_('Process'),
        to=Process,
        on_delete=models.CASCADE
    )
    state = models.CharField(max_length=100, choices=EXECUTION_STATES, default=EXECUTION_STATE_PENDING)
    started = models.DateTimeField(default=timezone.now)
    finished = models.DateTimeField(default=None, blank=True, null=True)
    configuration_data = models.CharField(max_length=10000, default=None, blank=True, null=True)

    @property
    def configuration(self):
        return json.dumps(self.configuration_data)

    @configuration.setter
    def configuration(self, value):
        self.configuration_data = json.dumps(value)

    @property
    def interval(self):
        if self.started is not None and self.finished is not None:
            return self.finished - self.started
        else:
            return 0

    def ingest_data(self, **kwargs):
        data_frame = DataFrame.objects.create(execution=self)
        data_frame.raw_data = kwargs
        # data_frame.save()
        return data_frame

    def end(self):
        self.finished = timezone.now()
        self.state = EXECUTION_STATE_FINISHED
        self.save()
        return self


class DataFrame(models.Model):
    execution = models.ForeignKey(
        verbose_name=_('Execution'),
        to=Execution,
        on_delete=models.CASCADE
    )

    data = models.TextField(max_length=100000, default=None, null=True, blank=True)
    additional_data = models.TextField(max_length=10000, default=None, null=True, blank=True)
    indicators_data = models.TextField(max_length=10000, default=None, null=True, blank=True)
    markers_data = models.TextField(max_length=10000, default=None, null=True, blank=True)

    @property
    def raw_data(self):
        return json.loads(self.data)

    @raw_data.setter
    def raw_data(self, value):
        self.data = json.dumps(value)

    @property
    def additional(self):
        return None if self.additional_data is None else json.loads(self.additional_data)

    @additional.setter
    def additional(self, value):
        self.additional_data = json.dumps(value)

    @property
    def indicators(self):
        return None if self.indicators_data is None else json.loads(self.indicators_data)

    @indicators.setter
    def indicators(self, value):
        self.indicators_data = json.dumps(value)

    @property
    def markers(self):
        return None if self.additional_data is None else json.loads(self.markers)

    @markers.setter
    def markers(self, value):
        self.markers_data = json.dumps(value)

    def ingest_additional(self, **kwargs):
        self.additional = {**kwargs}
        # self.save()
        return self

    def ingest_indicators(self, **kwargs):
        self.indicators = {**kwargs}
        # self.save()
        return self

    def ingest_markers(self, **kwargs):
        self.markers_data = {**kwargs}
        # self.save()
        return self

    def flush(self):
        self.save()
        return self.execution
