import concurrent.futures
from django.shortcuts import render
from netmiko import ConnectHandler
from .forms import single_command_form
from dashboard.models import Device


def results(request):
    return render(request, 'commands/results.html')
    
def index(request):
    global username
    global password
    global command
    if request.method == 'POST':
        sc_form = single_command_form(request.POST)
        if sc_form.is_valid():
            outputList = []
            hostList = []
            mikoList = []
            username = sc_form.cleaned_data['username']
            password = sc_form.cleaned_data['password']
            command = sc_form.cleaned_data['command']
            deviceType = sc_form.cleaned_data['deviceType']
            deviceModel = sc_form.cleaned_data['deviceModel']
            deviceSite = sc_form.cleaned_data['deviceSite']
            host = sc_form.cleaned_data['host']
            if deviceType:
                typeFilter = Device.objects.filter(device_type__in=deviceType)
            else:
                typeFilter = Device.objects.filter(device_type__isnull=False)
            if deviceModel:
                modelFilter = Device.objects.filter(model__in=deviceModel)
            else:
                modelFilter = Device.objects.filter(model__isnull=False)
            if deviceSite:
                siteFilter = Device.objects.filter(site__in=deviceSite)
            else:
                siteFilter = Device.objects.filter(site__isnull=False)
            if host:
                hostFilter = Device.objects.filter(hostname__in=host)
            else:
                hostFilter = Device.objects.filter(hostname__isnull=False)

            deviceQuery = hostFilter.intersection(typeFilter, modelFilter, siteFilter, hostFilter)

            for obj in deviceQuery:
                hostList.append(obj.hostname)
                mikoList.append(obj.netmiko_device_type)
            with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
                cmdOutput = executor.map(showcmd, hostList, mikoList)

            for result in cmdOutput:
                outputList.append(result)

        return render(request, 'commands/results.html', {'output': outputList})

    else:
        sc_form = single_command_form()
    return render(request, 'commands/index.html', {'sc_form': sc_form})


def showcmd(i, d):

    # SSH settings
    ssh = {
        'device_type': d,
        'host': i,
        'username': username,
        'password': password,
    }

    # SSH to the device and run command
    cmd = command
    try:
        connect = ConnectHandler(**ssh)
        output = connect.send_command(cmd)
    except Exception:
        return f'\nERROR: Failed to connect to {i}\n'
    return f'\n! Command Output From {i}\n{output}'
