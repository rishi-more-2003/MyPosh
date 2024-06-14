from django import forms
from .models import Education, EstablishmentLocation, PEDetails, VendorDetails, ComitteeCount, CurrentClient

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

class CurrentClientForm(forms.ModelForm):
    class Meta:
        model = CurrentClient
        exclude = ['user']


