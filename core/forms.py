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

class EnrollmentForm(forms.Form):
    client = forms.ModelChoiceField(queryset=Enrollment._meta.get_field('client').related_model.objects.all())
    program = forms.ModelMultipleChoiceField(
        queryset=HealthProgram.objects.all(),
        widget=forms.CheckboxSelectMultiple  # or SelectMultiple
    )