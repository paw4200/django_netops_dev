import concurrent.futures
import networkx as nx
import pydot
from django.shortcuts import render
from netmiko import ConnectHandler
from .forms import cdp_map_form
from dashboard.models import Device


def map(request):
    return render(request, 'discover/map.html')

def index(request):
    global username
    global password
    
    if request.method == 'POST':
        cdp_form = cdp_map_form(request.POST)
        if cdp_form.is_valid():
            global G
            G = nx.Graph()
            hostList = []
            mikoList = []
            username = cdp_form.cleaned_data['username']
            password = cdp_form.cleaned_data['password']
            deviceSite = cdp_form.cleaned_data['deviceSite']
            host = cdp_form.cleaned_data['host']
            if deviceSite:
                siteFilter = Device.objects.filter(site__in=deviceSite)
            else:
                siteFilter = Device.objects.filter(site__isnull=False)
            if host:
                hostFilter = Device.objects.filter(hostname__in=host)
            else:
                hostFilter = Device.objects.filter(hostname__isnull=False)

            deviceQuery = hostFilter.intersection(siteFilter, hostFilter)

            for obj in deviceQuery:
                hostList.append(obj.hostname)
                mikoList.append(obj.netmiko_device_type)

            with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
                cdpOutput = executor.map(cdpMap, hostList, mikoList)

            for result in cdpOutput:
                G.add_edges_from(result)
            cdp_dot = nx.nx_pydot.to_pydot(G)

        return render(request, 'discover/map.html', {'cdp_dot': cdp_dot})

    else:
        cdp_form = cdp_map_form()
    return render(request,'discover/index.html', {'cdp_form': cdp_form})

def cdpMap(i, d):

    # SSH settings
    ssh = {
        'device_type': d,
        'host': i,
        'username': username,
        'password': password,
    }

    edge_list = []

    cmd = "show cdp neighbors"
    try:
        connect = ConnectHandler(**ssh)
        output = connect.send_command(cmd, use_textfsm=True)
    except Exception:
        return

    for item in output:
        phone = 'IP Phone'
        plat = item.get('platform')
        if plat not in phone:
            n = item.get('neighbor')
            edge_list.append((i.strip(), n.rstrip(".swacorp.com")))
    return edge_list