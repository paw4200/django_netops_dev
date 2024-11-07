from django.contrib import admin
from import_export import resources
from .models import Device
from import_export.admin import ImportExportModelAdmin


class DeviceResource(resources.ModelResource):

    class Meta:
        model = Device

class DeviceAdmin(ImportExportModelAdmin):
    resource_classes = [DeviceResource]

admin.site.register(Device, DeviceAdmin)