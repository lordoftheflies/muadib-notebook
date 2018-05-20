import logging

from rest_framework import viewsets, permissions, renderers
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from instrumentation import serializers as instrumentation_serializers
from instrumentation import models as instumentation_models
from instrumentation import tasks as instumentation_tasks

logger = logging.getLogger(__name__)


# Create your views here.
#
# @api_view(['GET'])
# def active_resources_view(request):
#     try:
#         response = instumentation_tasks.active_resources.delay()
#         # response = run_task.delay(start=1, stop=1, step=1)
#         return Response(response.get(instumentation_tasks.ConsoleCommandModel.TIMEOUT))
#     except TimeoutError as e:
#         logger.warning('Terminal timeout expired (%s)' % str(e))
#         return Response([])
#
#
# @api_view(['GET'])
# def ping_view(request, resource_name):
#     try:
#         response = instumentation_tasks.run_task.apply_async(
#             queue=resource_name,
#             exchange='equipment',
#             # routing_key='%s' % resource_name,
#             kwargs=dict(start=1, stop=10, step=1)
#         )
#         return Response(response.get(instumentation_tasks.ConsoleCommandModel.TIMEOUT))
#     except TimeoutError as e:
#         logger.warning('Terminal timeout expired (%s)' % str(e))
#         return Response([])
#

class EquipmentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = instumentation_models.Equipment.objects.all()
    serializer_class = instrumentation_serializers.EquipmentSerializer
    permission_classes = [permissions.AllowAny]

    @action(
        detail=True,
        url_path='properties',
        url_name='properties',
        renderer_classes=[
            renderers.BrowsableAPIRenderer,
            renderers.JSONRenderer,
            renderers.StaticHTMLRenderer,
            renderers.DocumentationRenderer
        ]
    )
    def properties(self, request, *args, **kwargs):
        equipment_entity = self.get_object()
        return Response(instrumentation_serializers.EquipmentConfigurationSerializer(equipment_entity).data)


class ProcessViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = instumentation_models.Process.objects.all()
    serializer_class = instrumentation_serializers.ProcessSerializer
    permission_classes = [permissions.AllowAny]

    @action(
        detail=True,
        url_path='configuration',
        url_name='configuration',
        renderer_classes=[
            renderers.BrowsableAPIRenderer,
            renderers.JSONRenderer,
            renderers.StaticHTMLRenderer,
            renderers.DocumentationRenderer
        ]
    )
    def configuration(self, request, *args, **kwargs):
        process_entity = self.get_object()
        return Response(process_entity.configuration)

    @action(
        detail=True,
        url_path='executions',
        url_name='executions',
        renderer_classes=[
            renderers.BrowsableAPIRenderer,
            renderers.JSONRenderer,
            renderers.StaticHTMLRenderer,
            renderers.DocumentationRenderer
        ]
    )
    def executions(self, request, *args, **kwargs):
        process_entity = self.get_object()
        return Response(instrumentation_serializers.ExecutionInfoSerializer(process_entity.executions, many=True).data)

    @action(
        detail=True,
        url_path='execute',
        url_name='execute',
        renderer_classes=[
            renderers.BrowsableAPIRenderer,
            renderers.JSONRenderer,
            renderers.StaticHTMLRenderer,
            renderers.DocumentationRenderer
        ]
    )
    def execute(self, request, *args, **kwargs):
        try:

            process_entity = self.get_object()
            r = instumentation_tasks.process_execute_task.s(*args, **kwargs).apply_async(
                queue=process_entity.name,
                exchange=instumentation_models.Process.EXCHANGE_NAME,
                routing_key='%s' % process_entity.name
            )
            execution = r.get(timeout=60)
            return Response(execution)
        except TimeoutError as te:
            return Response(dict(error=str(te)))


class ExecutionViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = instumentation_models.Execution.objects.all()
    serializer_class = instrumentation_serializers.ExecutionSerializer
    permission_classes = [permissions.AllowAny]
    #
    # @action(detail=True, renderer_classes=[renderers.BrowsableAPIRenderer, renderers.JSONRenderer])
    # def schema(self, request, *args, **kwargs):
    #     equipment_entity = self.get_object()
    #     return Response(SchemaSerializer(equipment_entity.schema).data)

#
# class StandardResultsSetPagination(PageNumberPagination):
#     page_size = 20
#     page_size_query_param = 'page_size'
#     max_page_size = 20
#
#
# # class ConsoleListAPIView(ListAPIView):
# #     serializer_class = ConsoleCommandSerializer
#
# class ConsoleViewSet(viewsets.ModelViewSet):
#     queryset = ConsoleCommandModel.objects.all().order_by('-request_timestamp')[:20]
#     serializer_class = ConsoleCommandSerializer
#     permission_classes = [permissions.AllowAny]
#
#     # pagination_class = StandardResultsSetPagination
#
#     def perform_create(self, serializer):
#
#         logger.info('Terminal[%s] readline: %s' % (
#             serializer.validated_data['resource'],
#             serializer.validated_data
#         ))
#         try:
#             response = terminal_task.apply_async(
#                 queue=serializer.validated_data['resource'],
#                 exchange='equipment',
#                 # routing_key='%s' % resource_name,
#                 args=[serializer.validated_data['request']]
#             ).get()
#             logger.info('Output: %s' % response)
#         except TimeoutError as e:
#             logger.warning('Terminal timeout expired', e)
#         except BaseException as e:
#             logger.error('Unknown error', e)
