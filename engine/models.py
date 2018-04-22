import json

from django.db import models
from django.utils.translation import gettext as _


# Create your models here.

class ProcessModel(models.Model):
    class Meta:
        verbose_name = _('Process')

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