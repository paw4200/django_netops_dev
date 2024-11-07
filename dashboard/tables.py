import django_tables2 as tables
from .models import Device


class DeviceTable(tables.Table):
    class Meta:
        model = Device
        attrs = {'class': 'paleblue'}
        exclude = ('id', 'mgmt_interface', 'device_type', 'sysobjectid', 'serial_number', 'netmiko_device_type', )