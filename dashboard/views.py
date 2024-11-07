from django.shortcuts import render
from django_tables2 import RequestConfig
from .models import Device
from .tables import DeviceTable


# Create your views here.
def index(request):
    all_devices = Device.objects.all()
    all_device_table = DeviceTable(all_devices)
    RequestConfig(request).configure(all_device_table)
    return render(request,'dashboard/index.html', {'table': all_device_table})
