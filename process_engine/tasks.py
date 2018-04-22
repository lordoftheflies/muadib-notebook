# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task


@shared_task
def configure(equipment_id, **kwargs):
    return True


@shared_task
def status(equipment_id):
    return dict(
        id=equipment_id
    )
