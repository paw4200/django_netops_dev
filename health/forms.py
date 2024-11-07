from django import forms


class health_form(forms.Form):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'off'}))