from django import forms
from .models import HealthProgram
from .models import Client

class HealthProgramForm(forms.ModelForm):
    class Meta:
        model = HealthProgram
        fields = ['name', 'description']

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'age', 'gender', 'contact']        
