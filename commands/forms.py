from django import forms
from dashboard.models import Device
from .vars.form_vars import TypeChoices, ModelChoices, SiteChoices


class single_command_form(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    command = forms.CharField()
    host = forms.ModelMultipleChoiceField(queryset=Device.objects.exclude(netmiko_device_type='NA'), required=False)
    deviceType = forms.MultipleChoiceField(choices=TypeChoices, required=False)
    deviceModel = forms.MultipleChoiceField(choices=ModelChoices, required=False)
    deviceSite = forms.MultipleChoiceField(choices=SiteChoices, required=False)

    class Meta:
        model = Device