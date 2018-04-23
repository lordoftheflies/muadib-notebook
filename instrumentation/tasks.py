# Create your tasks here
from __future__ import absolute_import, unicode_literals

import celery
from celery import shared_task
from celery.utils.log import get_task_logger

from instrumentation.models import EquipmentModel
from muadib import sio

logger = get_task_logger(__name__)


class ProcessTask(celery.Task):

    def on_success(self, retval, task_id, args, kwargs):
        super().on_success(retval, task_id, args, kwargs)
        print('{0!r} success: {1!r}'.format(task_id, retval))

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        super().on_failure(exc, task_id, args, kwargs, einfo)
        print('{0!r} failed: {1!r}'.format(task_id, exc))


class EquipmentTask(celery.Task):

    def on_success(self, retval, task_id, args, kwargs):
        super().on_success(retval, task_id, args, kwargs)
        sio.emit('state', dict(
            task_id=task_id,
            state=retval,
            args=args,
            kwargs=kwargs
        ))
        print('{0!r} success: {1!r}'.format(task_id, retval))

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        super().on_failure(exc, task_id, args, kwargs, einfo)
        sio.emit('state', dict(
            task_id=task_id,
            state=str(exc),
            args=args,
            kwargs=kwargs
        ))

@shared_task(base=EquipmentTask)
def ping(equipment_id):
    return EquipmentModel.objects.get(id=equipment_id)


@shared_task
def configure(equipment_id, **kwargs):
    return True


@shared_task
def status(equipment_id):
    return dict(
        id=equipment_id
    )


@shared_task(base=ProcessTask)
def execute(*args, **kwargs):
    print('-----------------------')
    print('Positional: %s' % args)
    print('Key-values: %s' % kwargs)
