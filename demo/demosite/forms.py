from django import forms
from django.db import models
from demosite.models import KeyTable

class KeyForm(forms.ModelForm):
    apart_name = forms.CharField(label="Apartment Name", max_length=200)
    apart_addr = forms.CharField(label="Apartment Address", max_length=200)
    class Meta:
        model = KeyTable
        fields = "__all__"
