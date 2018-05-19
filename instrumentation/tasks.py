from __future__ import absolute_import, unicode_literals

import json
import time
import traceback

import celery
import visa
from asgiref.sync import async_to_sync
from celery import shared_task
from celery.signals import task_prerun, task_postrun
from celery.utils.log import get_task_logger
from channels.layers import get_channel_layer
from django.db import transaction
from django.utils import timezone

from instrumentation.drivers import dm
from instrumentation.models import Execution, Process, DataFrame

logger = get_task_logger(__name__)


class InstrumentationContextMixin(object):

    @property
    def slug(self) -> str:
        return self.request.delivery_info['routing_key']


class ConfigurableMixin(object):

    @property
    def configuration(self):
        return self._configuration

    @configuration.setter
    def configuration(self, value):
        self._configuration = value

    def override_configuration(self, **kwargs) -> dict:
        """
        Override equipment configuration
        :param kwargs:
        :return: Current configuration key-value parameters.
        """
        params = dict()
        for k in kwargs.keys():
            params[k] = kwargs[k]
        return params

    def update_configuration(self, **kwargs):
        self.configuration = self.override_configuration(**kwargs)
        return self.configuration

    def filter_include(self, *args):
        return {a: self._configuration[args] if a in self._configuration.keys() else None for a in args}


#
# class PersistenceContextMixin(ConfigurableMixin):
#
#     @property
#     def entity(self) -> EquipmentModel:
#         return self._entity
#
#     @entity.setter
#     def entity(self, value: EquipmentModel):
#         self._entity = value
#
#     def persist_command(self, **kwargs) -> ConsoleCommandModel:
#         return ConsoleCommandModel.objects.create(**kwargs)
#
#     def persist_equipment(self, **kwargs) -> EquipmentModel:
#         self.entity.configuration = kwargs
#         self.entity.save()
#         return self.entity
#
#     def load_configuration(self) -> dict:
#         self.entity = EquipmentModel.objects.get(distinguished_name=self.slug)
#         self.configuration = self.entity.configuration
#         return self.configuration
#
#     def save_configuration(self) -> dict:
#         self.entity.configuration = self.configuration
#         self.entity.save()
#         return self.configuration
#

class DeviceContextMixin(object):

    @property
    def resource(self) -> visa.Resource:
        return self._resource

    @resource.setter
    def resource(self, value: visa.Resource):
        self._resource = value

    def __enter__(self):
        self._lock = self.resource.lock()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.resource.unlock()
        self._lock = None


class CausalContextMixin(object):

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

    def now(self):
        return timezone.now()

    def format_timestamp(self, d):
        return d.strftime("%Y-%m-%dT%H:%M:%S.%f")


class RealtimeObserverMixin(object):

    @property
    def socket_name(self) -> str:
        return self._socket_name

    @socket_name.setter
    def socket_name(self, value: str):
        self._socket_name = value

    def emit_output(self, **kwargs):
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(self.socket_name, {
            "type": "resource_terminal",
            "message": kwargs
        })

    def emit_error(self, **kwargs):
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(self.socket_name, {
            "type": "resource_terminal",
            "error": kwargs
        })


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
            task.load_configuration()
        logger.info('ENTITY: %s' % task.entity.id)

        task.begin_timestamp = task.now()
        task.socket_name = 'terminal_' + task.slug

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
            task.save_configuration()
    except BaseException as e:
        traceback.print_exc()


#
# # Create your tasks here
# class EquipmentTask(celery.Task, InstrumentationContextMixin, PersistenceContextMixin, DeviceContextMixin,
#                     CausalContextMixin, RealtimeObserverMixin):
#
#     def __init__(self) -> None:
#         super().__init__()
#         self._resource = None
#         self._lock = None
#         self._entity = None
#         self.persisted = True
#         self.realtime = True
#
#         self._begin_ts = None
#         self._end_ts = None
#
#     def resolve_command(self, *args, **kwargs):
#         command_template = ' '.join(args)
#         return command_template % kwargs
#
#     def on_success(self, retval, task_id, args, kwargs):
#         try:
#             self.end_timestamp = self.now()
#
#             super().on_success(retval, task_id, args, kwargs)
#
#             source = self.resolve_command(*args, **kwargs)
#
#             command_entity_options = dict(
#                 request_timestamp=self.begin_timestamp,
#                 response_timestamp=self.end_timestamp,
#                 equipment=self.entity,
#                 request=source,
#                 response='ok',
#                 error=None,
#             )
#             command_transfer_options = dict(
#                 request_timestamp=self.format_timestamp(self.begin_timestamp),
#                 response_timestamp=self.format_timestamp(self.end_timestamp),
#                 equipment=self.entity.id,
#                 slug=self.slug,
#                 name=self.entity.display_name,
#                 request=source,
#                 response='ok',
#                 error=None,
#             )
#
#             if self.realtime:
#                 self.emit_output(**command_transfer_options)
#                 logger.info("Command emitted successfully: %s" % command_transfer_options)
#
#             if self.persisted:
#                 with transaction.atomic() as t:
#                     command_entity = self.persist_command(**command_entity_options)
#                     logger.info("Command persisted successfully: %s" % command_entity_options)
#
#             logger.info("Command executed successfully: %s" % source)
#         except BaseException as e:
#             traceback.print_exc()
#
#     def on_failure(self, exc, task_id, args, kwargs, einfo):
#         try:
#             self.end_timestamp = self.now()
#
#             super().on_failure(exc, task_id, args, kwargs, einfo)
#
#             command_options = dict(
#                 request_timestamp=self.format_timestamp(self._begin_ts),
#                 response_timestamp=self.format_timestamp(self._end_ts),
#                 equipment=self.entity,
#                 request=self.resolve_command(*args, **kwargs),
#                 response=None,
#                 error=einfo,
#             )
#
#             if self.realtime:
#                 self.emit_output(**command_options)
#                 logger.info("Command emitted successfully: %s" % command_options)
#
#             if self.persisted:
#                 with transaction.atomic() as t:
#                     command_entity = self.persist_command(**command_options)
#                     logger.info("Command persisted successfully: %s" % command_options)
#
#             logger.info("Command execution failed: %s" % command_options)
#         except BaseException as e:
#             traceback.print_exc()

#
# @shared_task(base=EquipmentTask, bind=True)
# def terminal_task(self, *args, **kwargs):
#     print('%s << %s' % (self.slug, self.resolve_command(*args, **kwargs)))
#     return True
#
#
# @shared_task(base=EquipmentTask, bind=True)
# def variable_input_task(self, name, value, **kwargs):
#     try:
#         # self.entity.attribute_command(name=name, value=value)
#         kwargs[name] = value
#         return kwargs
#     except:
#         traceback.print_exc()
#
#
# @shared_task(base=EquipmentTask, bind=True)
# def variable_output_task(self, name, data, **kwargs):
#     try:
#         # self.entity.attribute_command(name=name, value=value)
#         kwargs[name] = data[name]
#         return kwargs
#     except:
#         traceback.print_exc()
#
#
# @shared_task(base=EquipmentTask, bind=True)
# def trace_task(self, output='trace', **kwargs):
#     try:
#         # self.entity.attribute_command(name=name, value=value)
#         kwargs[output] = 'Ez egy trace'
#         logger.info('Trace %s' % kwargs)
#
#         return kwargs
#     except:
#         traceback.print_exc()
#
#
# @shared_task(base=EquipmentTask, bind=True)
# def configure_task(self, **kwargs):
#     try:
#         response = chain(*[variable_input_task.s(self=self, name=k, value=kwargs[k]) for k in kwargs.keys()])
#         logger.info('Configure %s' % kwargs)
#
#         return response
#     except:
#         traceback.print_exc()
#
#
# @shared_task(base=EquipmentTask, bind=True)
# def process_task(self, **kwargs):
#     """
#     Process raw data to context
#     :param self:
#     :param kwargs:
#     :return:
#     """
#     try:
#         logger.info('Process %s' % kwargs)
#         return kwargs
#     except:
#         traceback.print_exc()
#
#
# @shared_task(base=EquipmentTask, bind=True)
# def aggregate_task(self, **kwargs):
#     """
#     Aggregate context data
#     :param self:
#     :param kwargs:
#     :return:
#     """
#     try:
#         response = chain(*[variable_output_task.s(self=self, name=k, value=kwargs[k]) for k in kwargs.keys()])
#         logger.info('Aggreate %s' % kwargs)
#
#         return response
#     except:
#         traceback.print_exc()
#
#
# @shared_task(base=EquipmentTask, bind=True)
# def observe_task(self, **kwargs):
#     """
#     Observe data
#     :param self:
#     :param kwargs:
#     :return:
#     """
#     try:
#         logger.info('Observe %s' % kwargs)
#         return kwargs
#     except:
#         traceback.print_exc()
#
#
# @shared_task(base=EquipmentTask, bind=True)
# def visualize_task(self, **kwargs):
#     """
#
#     :param self:
#     :param kwargs:
#     :return:
#     """
#     try:
#         logger.info('Visualize %s' % kwargs)
#
#         return kwargs
#     except:
#         traceback.print_exc()
#
#
# @shared_task(base=EquipmentTask, bind=True)
# def step_task(self, **kwargs):
#     try:
#         res = chain(
#             process_task.s(**kwargs),
#             aggregate_task.s(session=kwargs),
#             visualize_task.s(chart=kwargs),
#             observe_task.s(channel="kka"))()
#         return res
#     except:
#         traceback.print_exc()
#
#
# @shared_task(base=EquipmentTask, bind=True)
# def run_task(self, start, stop, step, **kwargs):
#     try:
#         res = chain(
#             configure_task.s(**kwargs),
#             observe_task.s(channel="kka"),
#             *[step_task.s(
#                 index=i
#             ) for i in range(start, stop, step)],
#             observe_task.s(channel="kka")
#         )()
#         return res
#     except:
#         traceback.print_exc()


@shared_task
def status(equipment_id):
    return dict(
        id=equipment_id
    )


#
# @shared_task
# def terminal_input(resource_name, command):
#     ts = timezone.now()
#     print('%s << %s' % (resource_name, command))
#
#     from channels.layers import get_channel_layer
#     from asgiref.sync import async_to_sync
#     channel_layer = get_channel_layer()
#
#     async_to_sync(channel_layer.group_send)('terminal_' + resource_name, {
#         "type": "resource_terminal",
#         "message": ConsoleCommandSerializer(ConsoleCommandModel.objects.create(
#             request_timestamp=ts,
#             response_timestamp=timezone.now(),
#             equipment=EquipmentModel.objects.get(distinguished_name=resource_name),
#             request=command,
#             response='ok',
#             error=None,
#         )).data
#     })
#     return dict(result='ok')


@shared_task
def terminal_output(*args, **kwargs):
    print('-----------------------')
    print('Positional: %s' % args)
    print('Key-values: %s' % kwargs)

    return dict(result='ok')


@shared_task
def active_resources():
    return dm.DRIVER_MANAGER.resources()


# ---------------------------------------------------------------------


class ProcessTask(celery.Task, ConfigurableMixin):

    def __init__(self) -> None:
        super().__init__()
        logger.info('Initialize process task')

    def __call__(self, *args, **kwargs):
        logger.info('Call process task')
        return super().__call__(*args, **kwargs)

    def on_success(self, retval, task_id, args, kwargs):
        super().on_success(retval, task_id, args, kwargs)

        logger.info('Process task success')
        logger.debug(retval)
        logger.debug(task_id)
        logger.debug(args)
        logger.debug(kwargs)

        self.persist_frame(**retval)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        super().on_failure(exc, task_id, args, kwargs, einfo)

        logger.info('Process task failure')

        logger.debug(exc)
        logger.debug(task_id)
        logger.debug(args)
        logger.debug(kwargs)
        logger.debug(einfo)

    def sleep(self, sleep_time):
        time.sleep(sleep_time)

    @property
    def execution(self) -> Execution:
        return self._execution

    @property
    def channel_layer(self):
        if self._channel_layer is None:
            self._channel_layer = get_channel_layer()

        return self._channel_layer

    def persist(self, **kwargs) -> DataFrame:
        self.execution.ingest_data(**kwargs)

    def create_instance(self, **kwargs) -> Execution:
        self._execution = Process.objects.begin(**kwargs)
        return self._execution

    def emit(self, room, resource, **kwargs):
        async_to_sync(self.channel_layer.group_send)(room, {
            "type": resource,
            "message": json.dumps(kwargs)
        })

    def emit_visualization(self, **kwargs):
        self.emit(room='execution_%s' % self.execution.id, resource='resource_graph', **kwargs)

    def emit_state(self, **kwargs):
        self.emit(room='queues', resource='resource_graph', **kwargs)


@shared_task(bind=True, base_task=ProcessTask)
def long_running_task(self, start, stop, step):
    self.override_configuration(
        frequency_f=100,
        span_f=4000,
        reference_level=-100,
    )

    for i in range(start, stop, step):
        self.update_state(state="PROGRESS", meta={'progress': 50})
        self.sleep(sleep_time=5)

    time.sleep(1)
    self.update_state(state="PROGRESS", meta={'progress': 90})
    time.sleep(1)
    return 'hello world: %i' % (a + b)


def configure_equipment(self, equipment_id, **kwargs):
    pass


@shared_task(bind=True, base_task=ProcessTask)
def run_process(self, *args, **kwargs):
    execution = self.create_instance(**kwargs)

