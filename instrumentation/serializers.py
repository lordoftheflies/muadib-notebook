from rest_framework import serializers

from instrumentation import models as instrumentation_models


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = instrumentation_models.Equipment
        fields = ['id', 'name', 'display_name', 'description', 'active']


class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = instrumentation_models.Process
        fields = ['id', 'name', 'display_name', 'description']

#
# class ConsoleCommandSerializer(serializers.ModelSerializer):
#
#     request_timestamp = serializers.DateTimeField(required=False, default=timezone.now())
#     response_timestamp = serializers.DateTimeField(required=False, default=timezone.now())
#
#     resource = serializers.CharField(required=True)
#
#     class Meta:
#         model = ConsoleCommandModel
#         fields = [
#             'id',
#             'request_timestamp',
#             'response_timestamp',
#             'resource',
#             'equipment',
#             'request',
#             'response',
#             'error'
#         ]
#
