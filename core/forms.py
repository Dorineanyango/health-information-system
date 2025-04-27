from django import forms
from .models import HealthProgram, Client, Enrollment

# Form for creating or updating a Health Program
class HealthProgramForm(forms.ModelForm):
    class Meta:
        model = HealthProgram
        fields = ['name', 'description'] 

# Form for registering 
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'age', 'gender', 'contact']  

# Form for enrolling a Client in one or more Health Programs
class EnrollmentForm(forms.Form):
    client = forms.ModelChoiceField(
        queryset=Enrollment._meta.get_field('client').related_model.objects.all(),
        label="Select Client"
    )
    # Multiple checkboxes to select programs
    program = forms.ModelMultipleChoiceField(
        queryset=HealthProgram.objects.all(),
        widget=forms.CheckboxSelectMultiple,  
        label="Select Programs"
    )