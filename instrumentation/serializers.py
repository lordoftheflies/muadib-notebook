from rest_framework import serializers

from instrumentation.models import EquipmentModel


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentModel
        fields = ['id', 'distinguished_name', 'display_name', 'description']

class SchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentModel
        fields = ['id', 'distinguished_name', 'display_name', 'description']
