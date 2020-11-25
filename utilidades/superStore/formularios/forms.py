from django import forms
from django.contrib.admin import widgets as wdadmin
from django.forms import widgets
class LoginUsuario(forms.Form):
    usuario=forms.CharField(label="Usuario:", widget=forms.TextInput(attrs={}))