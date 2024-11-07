from django.db import models


class Device(models.Model):
    hostname = models.CharField(max_length=255, unique=True)
    mgmt_ip = models.GenericIPAddressField(protocol='IPv4', null=True, unique=True)
    mgmt_interface = models.CharField(max_length=255)
    device_type = models.CharField(max_length=255)
    sysobjectid = models.CharField(max_length=255)
    vendor = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    software_version = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=255)
    site = models.CharField(max_length=255)
    netmiko_choices = [
        ('a10', 'a10'),
        ('accedian', 'accedian'),
        ('adtran_os', 'adtran_os'),
        ('adva_fsp150f2', 'adva_fsp150f2'),
        ('adva_fsp150f3', 'adva_fsp150f3'),
        ('alcatel_aos', 'alcatel_aos'),
        ('alcatel_sros', 'alcatel_sros'),
        ('allied_telesis_awplus', 'allied_telesis_awplus'),
        ('apresia_aeos', 'apresia_aeos'),
        ('arista_eos', 'arista_eos'),
        ('arris_cer', 'arris_cer'),
        ('aruba_os', 'aruba_os'),
        ('aruba_osswitch', 'aruba_osswitch'),
        ('aruba_procurve', 'aruba_procurve'),
        ('audiocode_66', 'audiocode_66'),
        ('audiocode_72', 'audiocode_72'),
        ('audiocode_shell', 'audiocode_shell'),
        ('avaya_ers', 'avaya_ers'),
        ('avaya_vsp', 'avaya_vsp'),
        ('broadcom_icos', 'broadcom_icos'),
        ('brocade_fastiron', 'brocade_fastiron'),
        ('brocade_fos', 'brocade_fos'),
        ('brocade_netiron', 'brocade_netiron'),
        ('brocade_nos', 'brocade_nos'),
        ('brocade_vdx', 'brocade_vdx'),
        ('brocade_vyos', 'brocade_vyos'),
        ('calix_b6', 'calix_b6'),
        ('casa_cmts', 'casa_cmts'),
        ('cdot_cros', 'cdot_cros'),
        ('centec_os', 'centec_os'),
        ('checkpoint_gaia', 'checkpoint_gaia'),
        ('ciena_saos', 'ciena_saos'),
        ('cisco_asa', 'cisco_asa'),
        ('cisco_ftd', 'cisco_ftd'),
        ('cisco_ios', 'cisco_ios'),
        ('cisco_nxos', 'cisco_nxos'),
        ('cisco_s200', 'cisco_s200'),
        ('cisco_s300', 'cisco_s300'),
        ('cisco_tp', 'cisco_tp'),
        ('cisco_viptela', 'cisco_viptela'),
        ('cisco_wlc', 'cisco_wlc'),
        ('cisco_xe', 'cisco_xe'),
        ('cisco_xr', 'cisco_xr'),
        ('cloudgenix_ion', 'cloudgenix_ion'),
        ('coriant', 'coriant'),
        ('dell_dnos9', 'dell_dnos9'),
        ('dell_force10', 'dell_force10'),
        ('dell_isilon', 'dell_isilon'),
        ('dell_os10', 'dell_os10'),
        ('dell_os6', 'dell_os6'),
        ('dell_os9', 'dell_os9'),
        ('dell_powerconnect', 'dell_powerconnect'),
        ('dell_sonic', 'dell_sonic'),
        ('dlink_ds', 'dlink_ds'),
        ('digi_transport', 'digi_transport'),
        ('eltex', 'eltex'),
        ('eltex_esr', 'eltex_esr'),
        ('endace', 'endace'),
        ('enterasys', 'enterasys'),
        ('ericsson_ipos', 'ericsson_ipos'),
        ('ericsson_mltn63', 'ericsson_mltn63'),
        ('ericsson_mltn66', 'ericsson_mltn66'),
        ('extreme', 'extreme'),
        ('extreme_ers', 'extreme_ers'),
        ('extreme_exos', 'extreme_exos'),
        ('extreme_netiron', 'extreme_netiron'),
        ('extreme_nos', 'extreme_nos'),
        ('extreme_slx', 'extreme_slx'),
        ('extreme_tierra', 'extreme_tierra'),
        ('extreme_vdx', 'extreme_vdx'),
        ('extreme_vsp', 'extreme_vsp'),
        ('extreme_wing', 'extreme_wing'),
        ('f5_linux', 'f5_linux'),
        ('f5_ltm', 'f5_ltm'),
        ('f5_tmsh', 'f5_tmsh'),
        ('flexvnf', 'flexvnf'),
        ('fortinet', 'fortinet'),
        ('generic', 'generic'),
        ('generic_termserver', 'generic_termserver'),
        ('hillstone_stoneos', 'hillstone_stoneos'),
        ('hp_comware', 'hp_comware'),
        ('hp_procurve', 'hp_procurve'),
        ('huawei', 'huawei'),
        ('huawei_olt', 'huawei_olt'),
        ('huawei_smartax', 'huawei_smartax'),
        ('huawei_vrp', 'huawei_vrp'),
        ('huawei_vrpv8', 'huawei_vrpv8'),
        ('ipinfusion_ocnos', 'ipinfusion_ocnos'),
        ('juniper', 'juniper'),
        ('juniper_junos', 'juniper_junos'),
        ('juniper_screenos', 'juniper_screenos'),
        ('keymile', 'keymile'),
        ('keymile_nos', 'keymile_nos'),
        ('linux', 'linux'),
        ('mellanox', 'mellanox'),
        ('mellanox_mlnxos', 'mellanox_mlnxos'),
        ('mikrotik_routeros', 'mikrotik_routeros'),
        ('mikrotik_switchos', 'mikrotik_switchos'),
        ('mrv_lx', 'mrv_lx'),
        ('mrv_optiswitch', 'mrv_optiswitch'),
        ('netapp_cdot', 'netapp_cdot'),
        ('netgear_prosafe', 'netgear_prosafe'),
        ('netscaler', 'netscaler'),
        ('nokia_srl', 'nokia_srl'),
        ('nokia_sros', 'nokia_sros'),
        ('oneaccess_oneos', 'oneaccess_oneos'),
        ('ovs_linux', 'ovs_linux'),
        ('paloalto_panos', 'paloalto_panos'),
        ('pluribus', 'pluribus'),
        ('quanta_mesh', 'quanta_mesh'),
        ('rad_etx', 'rad_etx'),
        ('raisecom_roap', 'raisecom_roap'),
        ('ruckus_fastiron', 'ruckus_fastiron'),
        ('ruijie_os', 'ruijie_os'),
        ('sixwind_os', 'sixwind_os'),
        ('sophos_sfos', 'sophos_sfos'),
        ('supermicro_smis', 'supermicro_smis'),
        ('teldat_cit', 'teldat_cit'),
        ('tplink_jetstream', 'tplink_jetstream'),
        ('ubiquiti_edge', 'ubiquiti_edge'),
        ('ubiquiti_edgerouter', 'ubiquiti_edgerouter'),
        ('ubiquiti_edgeswitch', 'ubiquiti_edgeswitch'),
        ('ubiquiti_unifiswitch', 'ubiquiti_unifiswitch'),
        ('vyatta_vyos', 'vyatta_vyos'),
        ('vyos', 'vyos'),
        ('watchguard_fireware', 'watchguard_fireware'),
        ('yamaha', 'yamaha'),
        ('zte_zxros', 'zte_zxros'),
        ('zyxel_os', 'zyxel_os'),
        ('NA', 'NA')
    ]
    netmiko_dict = {
        'Cisco ASA Firewall': 'cisco_asa',
        'Cisco IOS Switch': 'cisco_ios',
        'Cisco Nexus Switch': 'cisco_nxos',
        'Cisco Router': 'cisco_ios',
        'Cisco Voice Gateway': 'cisco_ios',
        'Cisco WLC': 'cisco_wlc',
        'F5 Load Balancer': 'f5_tmsh',
        'Palo Alto Firewall': 'paloalto_panos'
    }
    netmiko_device_type = models.CharField(max_length=30, choices=netmiko_choices, default='NA')

    def save(self, *args, **kwargs):
        self.hostname = self.hostname.lower()
        if '/' in self.hostname:
            self.hostname = self.hostname.split('/')[0]
        self.hostname = self.hostname.strip()
        if self.device_type in self.netmiko_dict:
            self.netmiko_device_type = self.netmiko_dict[self.device_type]
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.hostname    