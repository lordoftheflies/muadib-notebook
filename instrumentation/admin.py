from django.contrib import admin
from instrumentation.models import EquipmentModel, SchemaModel, SchemaAttributeModel


# Register your models here.

class SchemaAttributeInline(admin.StackedInline):
    model = SchemaAttributeModel
    extra = 0
    fields = [
        'distinguished_name',
        'display_name',
        'description',

        'data_type',
        'data_precision',
        'representation_type',
        'representation_precision',

        'constrait_minimum',
        'constrait_maximum',
        'constrait_pattern',
        'constrait_required'
    ]


@admin.register(SchemaModel)
class SchemaAdmin(admin.ModelAdmin):
    list_display = ['id', 'distinguished_name', 'display_name', 'description']
    inlines = [SchemaAttributeInline]


@admin.register(EquipmentModel)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'distinguished_name', 'display_name', 'description']
    pass
