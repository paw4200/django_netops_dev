import concurrent.futures
import cobra.mit.access
import cobra.mit.request
import cobra.mit.session
import cobra.model.fv
import cobra.model.pol
import cobra.model.event
from django.shortcuts import render
from netmiko import ConnectHandler
from .forms import health_form
from .vars.view_vars import crit_host_ios
from .vars.view_vars import crit_host_nxos


def results(request):
    return render(request, 'health/results.html')

# Create your views here.
def index(request):
    global username
    global password
    global aci_events
    aci_events = []

    if request.method == 'POST':
        crit_form = health_form(request.POST)
        aci_dampening_form = health_form(request.POST)
        if request.POST.get("crit_health_submit"):
            if crit_form.is_valid():
                username = crit_form.cleaned_data['username']
                password = crit_form.cleaned_data['password']
                outputList = []

                with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
                    iosOutput = executor.map(crit_ios, crit_host_ios)

                with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
                    nxosOutput = executor.map(crit_nxos, crit_host_nxos)

                for result in iosOutput:
                    outputList.append(result)

                for result in nxosOutput:
                    outputList.append(result)

            return render(request, 'health/results.html', {'output': outputList})

        if request.POST.get("aci_dampening_submit"):
            if aci_dampening_form.is_valid():
                username = aci_dampening_form.cleaned_data['username']
                password = aci_dampening_form.cleaned_data['password']

                url = f"https://w11-r-apic01"
                md = connect_to_apic(url, username, password)
                events = get_events(md)
                process_events(events)

                url = f"https://w11-s-apic01"
                md = connect_to_apic(url, username, password)
                events = get_events(md)
                process_events(events)

            return render(request, 'health/results.html', {'output': aci_events})

    else:
        crit_form = health_form()
        aci_dampening_form = health_form()
    return render(request, 'health/index.html', {'crit_form': crit_form, 'aci_dampening_form': aci_dampening_form})

def crit_ios(i):
    message=''
    established = 'Established'
    host = i.strip()
    up = 'up'
    zero = '0'
    admin = 'administratively down/down'
    neighbor_0 = '0.0.0.0'

    # SSH settings
    ssh = {
        'device_type': 'cisco_ios',
        'host': i,
        'username': username,
        'password': password,
    }

    # SSH to the device and run command
    #Gather VRF interfaces
    try:
        connect = ConnectHandler(**ssh)
        vrf_int = connect.send_command('show ip vrf interfaces', use_textfsm=True)
    except Exception:
        return f'ERROR: Failed to connect to {i}'

    #Gather BGP neighbors
    try:
        # connect = ConnectHandler(**ssh)
        bgp_neighbors = connect.send_command('show ip bgp vpnv4 all neighbors', use_textfsm=True)
    except Exception:
        return f'ERROR: Failed to connect to {i}'

    #Gather interfaces
    for item in vrf_int:
        int_name = item.get('interface')
        try:
            # connect = ConnectHandler(**ssh)
            interfaces = connect.send_command(f'show interfaces {int_name}', use_textfsm=True)
        except Exception:
            return f'ERROR: Failed to connect to {i}'

    #Check interface status
        int_link = interfaces[0].get('link_status')
        int_proto = interfaces[0].get('protocol_status')
        if (int_link != up or int_proto != up) and int_link != 'administratively down':
            message += f'ERROR: Host: {host} - Interface {int_name} - {int_link}/{int_proto}\n'

    #Check interface errors
        in_error = interfaces[0].get('input_errors')
        out_error = interfaces[0].get('output_errors')
        crc = interfaces[0].get('crc')
        frame = interfaces[0].get('frame')
        overrun = interfaces[0].get('overrun')
        abort = interfaces[0].get('abort')

        if (in_error and in_error != zero) or (out_error and out_error != zero):
            message += f'ERROR: Host: {host} - Interface {int_name} - Input errors: {in_error}, Output errors: {out_error}, CRC: {crc}, Frame: {frame}, Overrun: {overrun}, Abort: {abort}\n'
   
    #Check BGP neighbors
    for x in bgp_neighbors:
        n = x.get('remote_router_id')
        s = x.get('bgp_state')
        if s != established and s != admin and n != neighbor_0:
            message += f'ERROR: Host: {host} - Neighbor {n} - {s}\n'

    if message:
        return message
    else:
        return

def crit_nxos(i):
    message=''
    established = 'Established'
    host = i.strip()
    up = 'up'
    zero = '0'
    admin = 'Shut (Admin)'
    neighbor_0 = '0.0.0.0'

    # SSH settings
    ssh = {
        'device_type': 'cisco_nxos',
        'host': i,
        'username': username,
        'password': password,
    }

    # SSH to the device and run command
    #Gather VRF interfaces
    try:
        connect = ConnectHandler(**ssh)
        vrf_int = connect.send_command('show vrf interface', use_textfsm=True)
    except Exception:
        return f'ERROR: Failed to connect to {i}'

    #Gather BGP neighbors
    try:
        # connect = ConnectHandler(**ssh)
        bgp_neighbors = connect.send_command('show ip bgp neighbors vrf all', use_textfsm=True)
    except Exception:
        return f'ERROR: Failed to connect to {i}'

 #Gather interfaces
    for item in vrf_int:
        int_name = item.get('interface')
        if int_name != 'Null0':
            try:
                # connect = ConnectHandler(**ssh)
                interfaces = connect.send_command(f'show interface {int_name}', use_textfsm=True)
            except Exception:
                return f'ERROR: Failed to connect to {i}'

        #Check interface status
            int_link = interfaces[0].get('link_status')
            int_proto = interfaces[0].get('admin_state')
            if int_link != up and int_proto == up:
                message += f'ERROR: Host: {host} - Interface {int_name} - {int_link}\n'

        #Check interface errors
            in_error = interfaces[0].get('input_errors')
            out_error = interfaces[0].get('output_errors')

            if (in_error and in_error != zero) or (out_error and out_error != zero):
                message += f'ERROR: Host: {host} - Interface {int_name} - Input errors: {in_error}, Output errors: {out_error}\n'
 
    for x in bgp_neighbors:
        n = x.get('neighbor')
        s = x.get('bgp_state')
        if s != established and s!= admin and n != neighbor_0:
            message += f'ERROR: Host: {host} - Neighbor {n} - {s}\n'

    if message:
        return message
    else:
        return

def connect_to_apic(url, username, password):
    ls = cobra.mit.session.LoginSession(url, username, password)
    md = cobra.mit.access.MoDirectory(ls)
    md.login()
    return md

def get_events(md):
    query = cobra.mit.request.ClassQuery('faultRecord')
    query.pageSize = 50000
    events = md.query(query)
    return events

def process_events(events):
    for event in events:
        code_3696 = "3696"
        code_4311 = "4311"
        if code_3696 in event.code or code_4311 in event.code:
            aci_events.append(f"Event Code: {event.code}, Cause: {event.cause}, Description: {event.descr}")