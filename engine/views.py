from django.shortcuts import render
from rest_framework import viewsets, permissions, renderers
from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.
from engine.models import ProcessModel
from engine.serializers import ProcessSerializer


class ProcessViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = ProcessModel.objects.all()
    serializer_class = ProcessSerializer
    permission_classes = [permissions.AllowAny]

