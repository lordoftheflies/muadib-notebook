from django.utils import timezone
from rest_framework import serializers

from instrumentation.models import EquipmentModel, SchemaModel
from instrumentation.models import ConsoleCommandModel


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentModel
        fields = ['id', 'distinguished_name', 'display_name', 'description']


class SchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchemaModel
        fields = ['id', 'distinguished_name', 'display_name', 'description']


class ConsoleCommandSerializer(serializers.ModelSerializer):

    request_timestamp = serializers.DateTimeField(required=False, default=timezone.now())
    response_timestamp = serializers.DateTimeField(required=False, default=timezone.now())

    resource = serializers.CharField(required=True)

    class Meta:
        model = ConsoleCommandModel
        fields = [
            'id',
            'request_timestamp',
            'response_timestamp',
            'resource',
            'equipment',
            'request',
            'response',
            'error'
        ]

