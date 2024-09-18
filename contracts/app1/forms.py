from django import forms
from .models import Commune

class LocationForm(forms.Form):
    commune = forms.ModelChoiceField(queryset=Commune.objects.all(), required=True)
    daira = forms.CharField(max_length=100, required=False)
    wilaya = forms.CharField(max_length=100, required=False)
