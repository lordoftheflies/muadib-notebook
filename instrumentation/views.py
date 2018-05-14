import logging

from rest_framework import viewsets, permissions, renderers
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from instrumentation.models import EquipmentModel, SchemaModel, ConsoleCommandModel
from instrumentation.serializers import EquipmentSerializer, SchemaSerializer, ConsoleCommandSerializer
from instrumentation.tasks import active_resources
from instrumentation.tasks import terminal_input

logger = logging.getLogger(__name__)


# Create your views here.

@api_view(['GET'])
def active_resources_view(request):
    try:
        response = active_resources.delay()
        return Response(response.get(ConsoleCommandModel.TIMEOUT))
    except TimeoutError as e:
        logger.warning('Terminal timeout expired (%s)' % str(e))
        return Response([])


class SchemaViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = SchemaModel.objects.all()
    serializer_class = SchemaSerializer
    permission_classes = [permissions.AllowAny]


class EquipmentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = EquipmentModel.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [permissions.AllowAny]

    @action(
        detail=True,
        url_path='/configuration',
        url_name='equipment_configuration',
        renderer_classes=[
            renderers.BrowsableAPIRenderer,
            renderers.JSONRenderer
        ]
    )
    def configuration(self, request, *args, **kwargs):
        equipment_entity = self.get_object()
        return Response(equipment_entity.configuration)

    @action(detail=True, renderer_classes=[renderers.BrowsableAPIRenderer, renderers.JSONRenderer])
    def schema(self, request, *args, **kwargs):
        equipment_entity = self.get_object()
        return Response(SchemaSerializer(equipment_entity.schema).data)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 20


# class ConsoleListAPIView(ListAPIView):
#     serializer_class = ConsoleCommandSerializer

class ConsoleViewSet(viewsets.ModelViewSet):
    queryset = ConsoleCommandModel.objects.all().order_by('-request_timestamp')[:20]
    serializer_class = ConsoleCommandSerializer
    permission_classes = [permissions.AllowAny]

    # pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):

        logger.info('Terminal[%s] readline: %s' % (
            serializer.validated_data['resource'],
            serializer.validated_data
        ))
        try:
            response = terminal_input.delay(
                resource_name=serializer.validated_data['resource'],
                command=serializer.validated_data['request']
            ).get()
            logger.info('Output: %s' % response)
        except TimeoutError as e:
            logger.warning('Terminal timeout expired', e)
        except BaseException as e:
            logger.error('Unknown error', e)
