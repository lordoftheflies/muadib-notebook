from rest_framework import serializers

from engine.models import ProcessModel
from instrumentation.models import EquipmentModel


class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessModel
        fields = ['id', 'distinguished_name', 'display_name', 'description']
