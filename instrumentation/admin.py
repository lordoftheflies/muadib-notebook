from django.contrib import admin
from instrumentation import models as instrumentation_model


# Register your models here.

class EquipmentPropertyInline(admin.StackedInline):
    model = instrumentation_model.EquipmentProperty
    extra = 0
    fields = [
        'name',
        'display_name',
        'description',
        'default_value',
        'equipment'
    ]


class ProcessParameterInline(admin.StackedInline):
    model = instrumentation_model.ProcessParameter
    extra = 0
    fields = [
        'name',
        'display_name',
        'description',
        'default_value',
        'process'
    ]


@admin.register(instrumentation_model.Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'display_name', 'description', 'active']
    inlines = [EquipmentPropertyInline]


@admin.register(instrumentation_model.Process)
class ProcessAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'display_name', 'description']
    inlines = [ProcessParameterInline]
