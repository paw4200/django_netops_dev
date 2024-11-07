from django import forms
from dashboard.models import Device
from .vars.form_vars import SiteChoices

class cdp_map_form(forms.Form):
    type_list = ['Cisco Router', 'Cisco IOS Switch', 'Cisco Nexus Switch']
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    host = forms.ModelMultipleChoiceField(queryset=Device.objects.filter(device_type__in=type_list), required=False)
    deviceSite = forms.MultipleChoiceField(choices=SiteChoices, required=False)