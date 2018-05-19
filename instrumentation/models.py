import json
import logging
import traceback

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
# Create your models here.
from kombu import Queue, Exchange

logger = logging.getLogger(__name__)

ATTRIBUTE_REPRESENTATION_TYPE_TEXT = 'text'
ATTRIBUTE_REPRESENTATION_TYPE_NUMBER = 'number'
ATTRIBUTE_REPRESENTATION_TYPE_DATE = 'date'
ATTRIBUTE_REPRESENTATION_TYPES = [
    (ATTRIBUTE_REPRESENTATION_TYPE_DATE, _('Date')),
    (ATTRIBUTE_REPRESENTATION_TYPE_NUMBER, _('Number')),
    (ATTRIBUTE_REPRESENTATION_TYPE_TEXT, _('Text')),
]


class DataRepresentationMixin(models.Model):
    representation_type = models.CharField(
        verbose_name=_('Representation type'),
        max_length=20,
        choices=ATTRIBUTE_REPRESENTATION_TYPES,
        default=ATTRIBUTE_REPRESENTATION_TYPE_TEXT
    )
    representation_precision = models.IntegerField(
        verbose_name=_('Representation precision'),
        default=3
    )

    class Meta:
        abstract = True


class ValidationMixin(models.Model):
    constrait_minimum = models.FloatField(default=None, blank=True, null=True)
    constrait_maximum = models.FloatField(default=None, blank=True, null=True)
    constrait_pattern = models.CharField(max_length=100, default=None, blank=True, null=True)
    constrait_required = models.BooleanField(default=False)

    class Meta:
        abstract = True


class StronglyTypedMixin(models.Model):
    ATTRIBUTE_DATA_TYPE_STR = 'str'
    ATTRIBUTE_DATA_TYPE_FLOAT = 'float'
    ATTRIBUTE_DATA_TYPE_INT = 'int'
    ATTRIBUTE_DATA_TYPE_DATE = 'date'
    ATTRIBUTE_DATA_TYPE_TIME = 'time'
    ATTRIBUTE_DATA_TYPE_DATETIME = 'datetime'
    ATTRIBUTE_DATA_TYPE_PERIOD = 'period'
    ATTRIBUTE_DATA_TYPE_INTERVAL = 'interval'
    ATTRIBUTE_DATA_TYPES = [
        (ATTRIBUTE_DATA_TYPE_DATE, _('Date')),
        (ATTRIBUTE_DATA_TYPE_DATETIME, _('Datetime')),
        (ATTRIBUTE_DATA_TYPE_FLOAT, _('Float')),
        (ATTRIBUTE_DATA_TYPE_INT, _('Integer')),
        (ATTRIBUTE_DATA_TYPE_INTERVAL, _('Interval')),
        (ATTRIBUTE_DATA_TYPE_PERIOD, _('Period')),
        (ATTRIBUTE_DATA_TYPE_STR, _('String')),
        (ATTRIBUTE_DATA_TYPE_TIME, _('Time')),
    ]

    data_type = models.CharField(
        verbose_name=_('Data type'),
        max_length=20,
        choices=ATTRIBUTE_DATA_TYPES,
        default=ATTRIBUTE_DATA_TYPE_STR
    )
    data_default = models.CharField(
        verbose_name=_('Default value'),
        max_length=20,
        blank=True,
        default=None,
        null=True
    )
    data_precision = models.IntegerField(
        verbose_name=_('Data precision'),
        default=3
    )

    class Meta:
        abstract = True


class ContentMixin(models.Model):
    distinguished_name = models.CharField(
        verbose_name=_('Distinguished name'),
        max_length=100
    )

    display_name = models.CharField(
        verbose_name=_('Display name'),
        max_length=500,
        default=None,
        blank=True,
        null=True
    )

    description = models.TextField(
        verbose_name=_('Description'),
        max_length=5000,
        default=None,
        blank=True,
        null=True
    )

    class Meta:
        abstract = True


class EnumerationModel(ContentMixin):
    class Meta:
        verbose_name = _('Enumeration')


class ConstantModel(ContentMixin):
    class Meta:
        verbose_name = _('Constant')

    enumeration = models.ForeignKey(
        verbose_name=_('Enumeration'),
        to=EnumerationModel,
        on_delete=models.CASCADE
    )


class OperationModel(models.Model):
    class Meta:
        verbose_name = _('Operation')

    source = models.TextField(
        verbose_name=_('Source'),
        max_length=5000,
        default=None,
        blank=True,
        null=True
    )

    @property
    def parameters(self):
        return ParameterModel.objects.filter(owner__id=self.id)

    def build(self, **kwargs):
        try:
            return self.source % kwargs
        except BaseException as e:
            logger.warning('%s could not resolve source arguments %s' % (self.source, kwargs))
            traceback.print_exc()


class ParameterModel(ContentMixin, DataRepresentationMixin):
    class Meta:
        verbose_name = _('Parameter')

    owner = models.ForeignKey(
        verbose_name=_('Operation'),
        to=OperationModel,
        on_delete=models.CASCADE
    )


class SchemaModel(ContentMixin):
    class Meta:
        verbose_name = _('Schema')

    def __str__(self):
        return self.display_name

    @property
    def attributes(self):
        return SchemaAttributeModel.objects.filter(schema__id=self.id)

    @property
    def actions(self):
        return SchemaActionModel.objects.filter(schema__id=self.id)


class SchemaActionModel(ContentMixin):
    class Meta:
        verbose_name = _('Action')

    schema = models.ForeignKey(
        verbose_name=_('Schema'),
        to=SchemaModel,
        on_delete=models.CASCADE
    )

    operation = models.ForeignKey(
        verbose_name=_('Operation'),
        to=OperationModel,
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )


class SchemaAttributeModel(ContentMixin, DataRepresentationMixin, StronglyTypedMixin, ValidationMixin):
    class Meta:
        verbose_name = _('Attribute')

    schema = models.ForeignKey(
        verbose_name=_('Schema'),
        to=SchemaModel,
        on_delete=models.CASCADE
    )

    read_operation = models.ForeignKey(
        verbose_name=_('Read operation'),
        to=OperationModel,
        related_name='reads',
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    write_operation = models.ForeignKey(
        verbose_name=_('Write operation'),
        to=OperationModel,
        related_name='writes',
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    query_operation = models.ForeignKey(
        verbose_name=_('Query operation'),
        to=OperationModel,
        related_name='queries',
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )


class EquipmentModel(ContentMixin):
    class Meta:
        verbose_name = _('Equipment')

    def __str__(self):
        return self.display_name

    schema = models.ForeignKey(
        verbose_name=_('Schema'),
        to=SchemaModel,
        on_delete=models.CASCADE
    )

    _configuration = models.TextField(
        verbose_name=_('Configuration')
    )

    address = models.TextField(
        verbose_name=_('Address')
    )

    @property
    def configuration(self):
        return json.loads(self._configuration)

    @configuration.setter
    def configuration(self, value):
        self._configuration = json.dumps(value)

    def attribute(self, name):
        return SchemaAttributeModel.objects.filter(distinguished_name=name, schema=self.schema).first()

    def attache_queue(self) -> Queue:
        from muadib.celery import app
        originals = list(app.conf.task_queues) if app.conf.task_queues is not None else []

        exchange = Exchange('equipment', 'direct', durable=True)
        queue = Queue(
            name=self.distinguished_name,
            exchange=exchange,
            routing_key='%s.#' % self.distinguished_name)
        originals.append(queue)
        app.conf.update(
            task_queues=originals
        )
        return queue


class TerminalManager(models.Manager):

    def __init__(self) -> None:
        super().__init__()

    def output(self, line_buffer_size=None) -> list:
        return []


class ConsoleCommandModel(models.Model):
    TIMEOUT = 10

    request_timestamp = models.DateTimeField(default=timezone.now)
    response_timestamp = models.DateTimeField(default=None, null=True, blank=True)

    equipment = models.ForeignKey(EquipmentModel, blank=True, null=True, default=None, on_delete=models.CASCADE)

    request = models.CharField(max_length=1000, blank=True, null=True, default=None)
    response = models.CharField(max_length=1000, blank=True, null=True, default=None)
    error = models.CharField(max_length=1000, blank=True, null=True, default=None)

    @property
    def resource(self):
        if (self.equipment is not None):
            return self.equipment.distinguished_name
        else:
            return None

    @resource.setter
    def resource(self, value):
        self.equipment = EquipmentModel.objects.get(distinguished_name=value)
        self.save()


# ------------------------------------

class Content(models.Model):
    name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100, null=True, blank=True, default=None)
    description = models.CharField(max_length=1000, null=True, blank=True, default=None)

    class Meta:
        abstract = True

DATA_TYPE_TEXT = 'text'
DATA_TYPE_NUMBER = 'number'
DATA_TYPE_DATE = 'date'

DATA_TYPES = [
    (DATA_TYPE_DATE, _('Date')),
    (DATA_TYPE_NUMBER, _('Number')),
    (DATA_TYPE_TEXT, _('Text')),
]

class Process(Content):
    pass

    def begin(self):
        execution = Execution.objects.create(
            process=self
        )
        return execution



  class Parameter(Content):
    data_type = models.CharField(max_length=100, choices=DATA_TYPES, default=DATA_TYPE_TEXT)
    default_value = models.CharField(max_length=100, null=True, blank=True, default=None)


class Execution(models.Model):
    root_task_id = models.UUIDField(null=True, blank=True, default=None)
    process = models.ForeignKey(
        verbose_name=_('Process'),
        to=Process,
        on_delete=models.CASCADE
    )

    started = models.DateTimeField(default=timezone.now)
    finished = models.DateTimeField(default=None, blank=True, null=True)

    @property
    def interval(self):
        if self.started is not None and self.finished is not None:
            return self.finished - self.started
        else:
            return 0

    def ingest_data(self, **kwargs):
        data_frame = DataFrame.objects.create(execution=self)
        data_frame.raw = kwargs
        data_frame.save()

class DataFrame(models.Model):
    execution = models.ForeignKey(
        verbose_name=_('Execution'),
        to=Execution,
        on_delete=models.CASCADE
    )

    _raw = models.TextField(max_length=100000, default=None, null=True, blank=True)

    @property
    def raw(self):
        return json.loads(self._raw)

    @raw.setter
    def raw(self, value):
        self._raw = json.dumps(value)
