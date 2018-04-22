from django.contrib import admin

from engine.models import ProcessModel


# Register your models here.


@admin.register(ProcessModel)
class ProcessAdmin(admin.ModelAdmin):
    list_display = ['id', 'distinguished_name', 'display_name', 'description']
    pass
