import json

from django.db import models
from django.utils.translation import gettext as _


# Create your models here.
from kombu import Queue


class EnumerationModel(models.Model):
    class Meta:
        verbose_name = _('Enumeration')

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


class ConstantModel(models.Model):
    class Meta:
        verbose_name = _('Constant')

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
    enumeration = models.ForeignKey(
        verbose_name=_('Enumeration'),
        to=EnumerationModel,
        on_delete=models.CASCADE
    )


class SchemaModel(models.Model):
    class Meta:
        verbose_name = _('Schema')

    def __str__(self):
        return self.display_name

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


class SchemaAttributeModel(models.Model):
    ATTRIBUTE_REPRESENTATION_TYPE_TEXT = 'text'
    ATTRIBUTE_REPRESENTATION_TYPE_NUMBER = 'number'
    ATTRIBUTE_REPRESENTATION_TYPE_DATE = 'date'
    ATTRIBUTE_REPRESENTATION_TYPES = [
        (ATTRIBUTE_REPRESENTATION_TYPE_DATE, _('Date')),
        (ATTRIBUTE_REPRESENTATION_TYPE_NUMBER, _('Number')),
        (ATTRIBUTE_REPRESENTATION_TYPE_TEXT, _('Text')),
    ]

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

    class Meta:
        verbose_name = _('Attribute')

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

    schema = models.ForeignKey(
        verbose_name=_('Schema'),
        to=SchemaModel,
        on_delete=models.CASCADE
    )

    data_type = models.CharField(
        verbose_name=_('Data type'),
        max_length=20,
        choices=ATTRIBUTE_DATA_TYPES,
        default=ATTRIBUTE_DATA_TYPE_STR
    )
    data_precision = models.IntegerField(
        verbose_name=_('Data precision'),
        default=3
    )

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

    constrait_minimum = models.FloatField(default=None, blank=True, null=True)
    constrait_maximum = models.FloatField(default=None, blank=True, null=True)
    constrait_pattern = models.CharField(max_length=100, default=None, blank=True, null=True)
    constrait_required = models.BooleanField(default=False)


class EquipmentModel(models.Model):
    class Meta:
        verbose_name = _('Equipment')

    def __str__(self):
        return self.display_name

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

    schema = models.ForeignKey(
        verbose_name=_('Schema'),
        to=SchemaModel,
        on_delete=models.CASCADE
    )

    _configuration = models.TextField(
        verbose_name=_('Configuration')
    )

    @property
    def configuration(self):
        return json.loads(self._configuration)

    @configuration.setter
    def configuration(self, value):
        self._configuration = json.dumps(value)

    def attache_queue(self):
        from muadib.celery import app
        originals = list(app.conf.task_queues) if app.conf.task_queues is not None else []
        originals.append(Queue(self.distinguished_name, routing_key='%s.#' % self.distinguished_name))
        app.conf.update(
            task_queues=originals
        )
