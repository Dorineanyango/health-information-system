from django import forms
from .models import HealthProgram
from .models import Client
from .models import Enrollment

class HealthProgramForm(forms.ModelForm):
    class Meta:
        model = HealthProgram
        fields = ['name', 'description']

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'age', 'gender', 'contact'] 

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['client', 'program']  # Client and Program fields

    client = forms.ModelChoiceField(queryset=Client.objects.all(), empty_label="Select Client")
    program = forms.ModelMultipleChoiceField(queryset=HealthProgram.objects.all(), widget=forms.CheckboxSelectMultiple)               
