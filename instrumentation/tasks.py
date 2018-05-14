from __future__ import absolute_import, unicode_literals

import celery
from celery import shared_task
from celery.utils.log import get_task_logger

from instrumentation.drivers import dm

logger = get_task_logger(__name__)

# Create your tasks here

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

        print('{0!r} success: {1!r}'.format(task_id, retval))

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        super().on_failure(exc, task_id, args, kwargs, einfo)


@shared_task(base=EquipmentTask)
def update(slug, **kwargs):
    device = dm.device(dn=slug)
    return device.query(**kwargs)


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


@shared_task
def terminal_input(resource_name, command):
    print('%s << %s' % (resource_name, command))

    from channels.layers import get_channel_layer
    channel_layer = get_channel_layer()
    # from asgiref.sync import sync_to_async
    from asgiref.sync import async_to_sync
    async_to_sync(channel_layer.group_send)('terminal_' + resource_name, {
        "type": "resource_terminal",
        "message": command
    })
    return dict(result='ok')


@shared_task
def terminal_output(*args, **kwargs):
    print('-----------------------')
    print('Positional: %s' % args)
    print('Key-values: %s' % kwargs)

    return dict(result='ok')


@shared_task
def active_resources():
    return dm.DRIVER_MANAGER.resources()
