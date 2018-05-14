from __future__ import absolute_import, unicode_literals

import json
import traceback

import celery
import datetime
import visa
from celery import shared_task, current_task
from celery.signals import task_prerun, task_postrun
from celery.utils.log import get_task_logger
from django.db import transaction
from django.utils import timezone


from instrumentation.drivers import dm, DeviceManager
from instrumentation.models import ConsoleCommandModel, EquipmentModel
from instrumentation.serializers import ConsoleCommandSerializer

logger = get_task_logger(__name__)



@task_prerun.connect
def task_prerun_handler(signal=None, sender=None, task_id=None, task=None, *args, **kwargs):
    """
    Setup device context
    :param signal:
    :param sender:
    :param task_id:
    :param task:
    :param args:
    :param kwargs:
    :return:
    """
    try:
        logger.info('===================================')
        logger.info('TASK: %s[%s]' % (task.name, task_id))
        logger.info('DELIVERY: %s' % task.request.delivery_info)
        logger.info('Positional: %s' % list(args))
        logger.info('Key-values: %s' % json.dumps(kwargs))

        task.resource = dm.device(task.slug).resource
        logger.info('VISA: %s' % task.resource.resource_name)
        with transaction.atomic():
            task.entity = EquipmentModel.objects.get(distinguished_name=task.slug)
        logger.info('ENTITY: %s' % task.entity.id)

        task.begin_timestamp = task.now()

        logger.info('-----------------------------------')
    except BaseException as e:
        traceback.print_exc()


@task_postrun.connect()
def task_postrun(signal=None, sender=None, task_id=None, task=None, retval=None, state=None, *args, **kwargs):
    """
    Cleanup
    :param signal:
    :param sender:
    :param task_id:
    :param task:
    :param retval:
    :param state:
    :param args:
    :param kwargs:
    :return:
    """
    try:
        logger.info('-----------------------------------')
        logger.info('TASK: %s[%s]' % (task.name, task_id))
        logger.info('RETVAL: %s' % retval)
        logger.info('STATE: %s' % state)
        logger.info('===================================')

        task.end_timestamp = task.now()

        # task.resource
        with transaction.atomic():
            task.persist_configuration()
    except BaseException as e:
        traceback.print_exc()


# Create your tasks here

class ProcessTask(celery.Task):

    def on_success(self, retval, task_id, args, kwargs):
        super().on_success(retval, task_id, args, kwargs)
        print('{0!r} success: {1!r}'.format(task_id, retval))

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        super().on_failure(exc, task_id, args, kwargs, einfo)
        print('{0!r} failed: {1!r}'.format(task_id, exc))


class EquipmentTask(celery.Task):

    def __init__(self) -> None:
        super().__init__()
        self._resource = None
        self._lock = None
        self._entity = None
        self.persisted = True
        self.realtime = True

        self._begin_ts = None
        self._end_ts = None

    @property
    def slug(self) -> str:
        return self.request.delivery_info['routing_key']

    def __enter__(self):
        self._lock = self.resource.lock()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.resource.unlock()
        self._lock = None

    @property
    def begin_timestamp(self):
        return self._begin_ts

    @begin_timestamp.setter
    def begin_timestamp(self, value):
        self._begin_ts = value

    @property
    def end_timestamp(self):
        return self._end_ts

    @end_timestamp.setter
    def end_timestamp(self, value):
        self._end_ts = value

    @property
    def resource(self) -> visa.Resource:
        return self._resource

    @resource.setter
    def resource(self, value: visa.Resource):
        self._resource = value

    @property
    def entity(self) -> EquipmentModel:
        return self._entity

    @entity.setter
    def entity(self, value: EquipmentModel):
        self._entity = value

    def resolve_command(self, *args, **kwargs):
        command_template = ' '.join(args)
        return command_template % kwargs

    def emit(self, **kwargs):

        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)('terminal_' + self.slug, {
            "type": "resource_terminal",
            "message": kwargs
        })

    def now(self):
        return timezone.now()

    def format_timestamp(self, d):
        return d.strftime("%Y-%m-%dT%H:%M:%S.%f")

    def on_success(self, retval, task_id, args, kwargs):
        try:
            self.end_timestamp = self.now()

            super().on_success(retval, task_id, args, kwargs)

            source = self.resolve_command(*args, **kwargs)

            command_entity_options = dict(
                request_timestamp=self.begin_timestamp,
                response_timestamp=self.end_timestamp,
                equipment=self.entity,
                request=source,
                response='ok',
                error=None,
            )
            command_transfer_options = dict(
                request_timestamp=self.format_timestamp(self.begin_timestamp),
                response_timestamp=self.format_timestamp(self.end_timestamp),
                equipment=self.entity.id,
                slug=self.slug,
                name=self.entity.display_name,
                request=source,
                response='ok',
                error=None,
            )

            if self.realtime:
                self.emit(**command_transfer_options)
                logger.info("Command emitted successfully: %s" % command_transfer_options)

            if self.persisted:
                with transaction.atomic() as t:
                    command_entity = self.persist_command(**command_entity_options)
                    logger.info("Command persisted successfully: %s" % command_entity_options)

            logger.info("Command executed successfully: %s" % source)
        except BaseException as e:
            traceback.print_exc()

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        try:
            self.end_timestamp = self.now()

            super().on_failure(exc, task_id, args, kwargs, einfo)

            command_options = dict(
                request_timestamp=self.format_timestamp(self._begin_ts),
                response_timestamp=self.format_timestamp(self._end_ts),
                equipment=self.entity,
                request=self.resolve_command(*args, **kwargs),
                response=None,
                error=einfo,
            )

            if self.realtime:
                from channels.layers import get_channel_layer
                from asgiref.sync import async_to_sync
                channel_layer = get_channel_layer()

                async_to_sync(channel_layer.group_send)('terminal_' + self.name, {
                    "type": "resource_terminal",
                    "error": command_options
                })

            if self.persisted:
                with transaction.atomic() as t:
                    command_entity = self.persist_command(
                        **command_options
                    )

            logger.info("Command execution failed: %s" % command_options)
        except BaseException as e:
            traceback.print_exc()

    def persist_command(self, **kwargs) -> ConsoleCommandModel:
        return ConsoleCommandModel.objects.create(**kwargs)

    def persist_configuration(self) -> EquipmentModel:
        self.entity.save()
        return self.entity


@shared_task(base=EquipmentTask, bind=True)
def terminal_task(self, *args, **kwargs):
    print('%s << %s' % (self.slug, self.resolve_command(*args, **kwargs)))
    return True


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


@shared_task
def terminal_input(resource_name, command):
    ts = timezone.now()
    print('%s << %s' % (resource_name, command))

    from channels.layers import get_channel_layer
    from asgiref.sync import async_to_sync
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)('terminal_' + resource_name, {
        "type": "resource_terminal",
        "message": ConsoleCommandSerializer(ConsoleCommandModel.objects.create(
            request_timestamp=ts,
            response_timestamp=timezone.now(),
            equipment=EquipmentModel.objects.get(distinguished_name=resource_name),
            request=command,
            response='ok',
            error=None,
        )).data
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
