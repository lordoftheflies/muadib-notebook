import os

import socketio
from django.shortcuts import render
from rest_framework import viewsets, permissions, renderers
from rest_framework.decorators import action
from rest_framework.response import Response

from instrumentation.models import EquipmentModel, SchemaModel
from instrumentation.serializers import EquipmentSerializer, SchemaSerializer


# Create your views here.

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

    @action(detail=True, renderer_classes=[renderers.BrowsableAPIRenderer])
    def configuration(self, request, *args, **kwargs):
        equipment_entity = self.get_object()
        return Response(equipment_entity.configuration)

    @action(detail=True, renderer_classes=[renderers.BrowsableAPIRenderer])
    def schema(self, request, *args, **kwargs):
        equipment_entity = self.get_object()
        return Response(equipment_entity.schema)

