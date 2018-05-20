from rest_framework import serializers

from instrumentation import models as instrumentation_models


class EquipmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = instrumentation_models.Equipment
        fields = ['id', 'name', 'display_name', 'description', 'active']


class EquipmentPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = instrumentation_models.EquipmentProperty
        fields = ['id', 'name', 'display_name', 'description', 'default_value', 'data_type']


class EquipmentConfigurationSerializer(serializers.ModelSerializer):
    properties = EquipmentPropertySerializer(many=True, read_only=True)

    class Meta:
        model = instrumentation_models.Equipment
        fields = ['id', 'name', 'display_name', 'description', 'active', 'properties']


class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = instrumentation_models.Process
        fields = ['id', 'name', 'display_name', 'description']

class ExecutionSerializer(serializers.ModelSerializer):
    process = ProcessSerializer(many=False)


    class Meta:
        model = instrumentation_models.Execution
        fields = ['id', 'process', 'state']


class ExecutionInfoSerializer(serializers.ModelSerializer):
    started = serializers.DateTimeField()
    finished = serializers.DateTimeField()

    class Meta:
        model = instrumentation_models.Execution
        fields = ['id', 'state','started', 'finished']

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
