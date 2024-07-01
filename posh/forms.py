from django import forms
from .models import Education, EstablishmentLocation, PEDetails, VendorDetails, ComitteeCount, CurrentClient, EmployeeCount
from group.models import Notice
import datetime

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['school', 'degree', 'field_of_study', 'start_date', 'end_date', 'grade', 'description']

class EstablishmentLocationForm(forms.ModelForm):
    class Meta:
        model = EstablishmentLocation
        exclude = ['username']

class PEDetailsForm(forms.ModelForm):
    class Meta:
        model = PEDetails
        exclude = ['username']

class VendorDetailsForm(forms.ModelForm):
    class Meta:
        model = VendorDetails
        exclude = ['username']

class ComitteeCountForm(forms.ModelForm):
    class Meta:
        model = ComitteeCount
        exclude = ['user']

class MemberCountForm(forms.ModelForm):
    class Meta:
        model = EmployeeCount
        exclude = ['user']

class CurrentClientForm(forms.ModelForm):
    class Meta:
        model = CurrentClient
        exclude = ['user']

class CreateAssignmentForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['notice_name', 'due_date', 'due_time', 'instructions']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'due_time': forms.TimeInput(attrs={'type': 'time'}),
        }
    
    notice_name = forms.CharField(max_length=50, label='Notice Name')
    due_date = forms.DateField(initial=datetime.date.today, label='Due Date', widget=forms.DateInput(attrs={'type': 'date'}))
    due_time = forms.TimeField(initial=datetime.time(10, 10), label='Due Time', widget=forms.TimeInput(attrs={'type': 'time'}))
    instructions = forms.CharField(label='Instructions', widget=forms.Textarea)
